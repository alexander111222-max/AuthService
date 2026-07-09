from httpx import AsyncClient


async def test_user_can_read_products(user_ac: AsyncClient):
    response = await user_ac.get("/mock/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_user_cannot_create_product(user_ac: AsyncClient):
    response = await user_ac.post("/mock/products")
    assert response.status_code == 403


async def test_user_cannot_delete_product(user_ac: AsyncClient):
    response = await user_ac.delete("/mock/products/1")
    assert response.status_code == 403


async def test_manager_can_read_products(manager_ac: AsyncClient):
    response = await manager_ac.get("/mock/products")
    assert response.status_code == 200


async def test_manager_can_create_product(manager_ac: AsyncClient):
    response = await manager_ac.post("/mock/products")
    assert response.status_code == 200


async def test_manager_cannot_delete_product(manager_ac: AsyncClient):
    response = await manager_ac.delete("/mock/products/1")
    assert response.status_code == 403


async def test_admin_can_delete_product(admin_ac: AsyncClient):
    response = await admin_ac.delete("/mock/products/1")
    assert response.status_code == 200


async def test_unauthorized_cannot_read(ac: AsyncClient):
    ac.cookies.clear()
    response = await ac.get("/mock/products")
    assert response.status_code == 401


async def test_user_can_read_orders(user_ac: AsyncClient):
    response = await user_ac.get("/mock/orders")
    assert response.status_code == 200


async def test_user_can_read_shops(user_ac: AsyncClient):
    response = await user_ac.get("/mock/shops")
    assert response.status_code == 200