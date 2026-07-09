import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "first_name, last_name, middle_name, email, password, password_confirm, reg_status, login_status",
    [
        ("Alex", "Kuznetsov","m_name", "e2e_user@test.com", "123456", "123456", 200, 200),
        ("Alex", "Kuznetsov","m_name", "e2e_user@test.com", "123456", "123456", 409, 200),
        ("Alex", "Kuznetsov","m_name", "e2e_user2@test.com", "123456", "wrong", 400, 404),
    ],
)
async def test_register_login_logout(
    first_name, last_name, middle_name, email, password, password_confirm,
    reg_status, login_status, ac: AsyncClient
):
    response = await ac.post("/auth/register", json={
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "email": email,
        "password": password,
        "password_confirm": password_confirm,
    })
    assert response.status_code == reg_status

    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == login_status

    if login_status == 200:
        assert "access_token" in response.cookies
        ac.cookies.set("access_token", response.cookies.get("access_token"))
        ac.cookies.set("refresh_token", response.cookies.get("refresh_token"))

        response = await ac.post("/auth/logout")
        assert response.status_code == 200


async def test_full_auth_flow(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "first_name": "Full",
        "last_name": "Kuznetsov",
        "middle_name": "m_name",
        "email": "full_test@test.com",
        "password": "123456",
        "password_confirm": "123456",
    })
    assert response.status_code == 200

    response = await ac.post("/auth/login", json={"email": "full_test@test.com", "password": "123456"})
    assert response.status_code == 200
    ac.cookies.set("access_token", response.cookies.get("access_token"))
    ac.cookies.set("refresh_token", response.cookies.get("refresh_token"))

    response = await ac.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] == "full_test@test.com"

    response = await ac.post("/auth/refresh")
    assert response.status_code == 200
    assert "access_token" in response.cookies

    response = await ac.post("/auth/logout")
    assert response.status_code == 200
    ac.cookies.clear()

    response = await ac.get("/users/me")
    assert response.status_code == 401