from httpx import AsyncClient


async def test_get_all_roles(admin_ac: AsyncClient):
    response = await admin_ac.get("/admin/roles")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


async def test_get_all_roles_forbidden(user_ac: AsyncClient):
    response = await user_ac.get("/admin/roles")
    assert response.status_code == 403


async def test_get_role_by_id(admin_ac: AsyncClient):
    roles = await admin_ac.get("/admin/roles")
    role_id = roles.json()[0]["id"]

    response = await admin_ac.get(f"/admin/roles/{role_id}")
    assert response.status_code == 200
    assert "name" in response.json()


async def test_get_role_not_found(admin_ac: AsyncClient):
    response = await admin_ac.get("/admin/roles/99999")
    assert response.status_code == 404


