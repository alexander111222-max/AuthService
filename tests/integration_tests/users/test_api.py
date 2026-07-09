from httpx import AsyncClient


async def test_get_me(user_ac: AsyncClient):
    response = await user_ac.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "first_name" in data


async def test_get_me_unauthorized(ac: AsyncClient):
    ac.cookies.clear()
    response = await ac.get("/users/me")
    assert response.status_code == 401


async def test_edit_me(user_ac: AsyncClient):
    response = await user_ac.patch("/users/me", json={"first_name": "Updated"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"


async def test_edit_me_duplicate_email(user_ac: AsyncClient, admin_ac: AsyncClient):
    # пытаемся поставить email который уже занят админом
    response = await user_ac.patch("/users/me", json={"email": "admin@test.com"})
    assert response.status_code == 409


async def test_change_user_role(admin_ac: AsyncClient, user_ac: AsyncClient):
    # получаем id юзера
    me = await user_ac.get("/users/me")
    user_id = me.json()["id"]

    # получаем id роли manager
    roles = await admin_ac.get("/admin/roles")
    manager_role = next(r for r in roles.json() if r["name"] == "manager")

    response = await admin_ac.patch(f"/users/admin/{user_id}/role", json={"role_id": manager_role["id"]})
    assert response.status_code == 200


async def test_change_role_forbidden_for_user(user_ac: AsyncClient):
    response = await user_ac.patch("/users/admin/1/role", json={"role_id": 1})
    assert response.status_code == 403


async def test_delete_me(ac: AsyncClient):
    await ac.post("/auth/register", json={
        "first_name": "Delete",
        "last_name": "Delete",
        "middle_name": "Delete",
        "email": "delete_me@test.com",
        "password": "123456",
        "password_confirm": "123456",
    })
    response = await ac.post("/auth/login", json={"email": "delete_me@test.com", "password": "123456"})
    ac.cookies.set("access_token", response.cookies.get("access_token"))
    ac.cookies.set("refresh_token", response.cookies.get("refresh_token"))

    response = await ac.delete("/users/me")
    assert response.status_code == 200

    response = await ac.post("/auth/login", json={"email": "delete_me@test.com", "password": "123456"})
    assert response.status_code == 403