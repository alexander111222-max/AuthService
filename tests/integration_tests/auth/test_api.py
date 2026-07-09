import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "first_name, last_name, middle_name, email, password, password_confirm, status_code",
    [
        ("Alex", "Kuznetsov","m_name", "new_user@test.com", "123456", "123456", 200),
        ("Alex", "Kuznetsov","m_name", "new_user@test.com", "123456", "123456", 409),
        ("Alex", "Kuznetsov","m_name", "another@test.com", "123456", "wrong", 400),
    ],
)
async def test_register(first_name, last_name, middle_name, email, password, password_confirm, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "email": email,
        "password": password,
        "password_confirm": password_confirm,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("admin@test.com", "admin123", 200),
        ("admin@test.com", "wrongpass", 401),
        ("123123notex@test.com", "123456", 404),
    ],
)
async def test_login(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status_code

    if status_code == 200:
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies


async def test_logout(ac: AsyncClient):
    response = await ac.post("/auth/login", json={"email": "user@test.com", "password": "user123"})
    ac.cookies.set("access_token", response.cookies.get("access_token"))
    ac.cookies.set("refresh_token", response.cookies.get("refresh_token"))
    response = await ac.post("/auth/logout")
    assert response.status_code == 200


async def test_refresh(ac: AsyncClient):
    response = await ac.post("/auth/login", json={"email": "user@test.com", "password": "user123"})
    ac.cookies.set("access_token", response.cookies.get("access_token"))
    ac.cookies.set("refresh_token", response.cookies.get("refresh_token"))
    response = await ac.post("/auth/refresh")
    assert response.status_code == 200
    assert "access_token" in response.cookies


async def test_refresh_without_token(ac: AsyncClient):
    ac.cookies.clear()
    response = await ac.post("/auth/refresh")
    assert response.status_code == 401