from httpx import AsyncClient


async def test_get_all_entities(admin_ac: AsyncClient):
    response = await admin_ac.get("/admin/entities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


async def test_get_all_entities_forbidden(user_ac: AsyncClient):
    response = await user_ac.get("/admin/entities")
    assert response.status_code == 403


async def test_create_entity(admin_ac: AsyncClient):
    response = await admin_ac.post("/admin/entities", json={"name": "test_entity", "description": "test"})
    assert response.status_code == 200
    assert response.json()["name"] == "test_entity"


async def test_create_entity_duplicate(admin_ac: AsyncClient):
    await admin_ac.post("/admin/entities", json={"name": "duplicate_entity", "description": "test"})
    response = await admin_ac.post("/admin/entities", json={"name": "duplicate_entity", "description": "test"})
    assert response.status_code == 409


async def test_edit_entity(admin_ac: AsyncClient):
    create = await admin_ac.post("/admin/entities", json={"name": "edit_entity", "description": "old"})
    entity_id = create.json()["id"]

    response = await admin_ac.patch(f"/admin/entities/{entity_id}", json={"description": "new"})
    assert response.status_code == 200
    assert response.json()["description"] == "new"


async def test_delete_entity(admin_ac: AsyncClient):
    create = await admin_ac.post("/admin/entities", json={"name": "delete_entity", "description": "test"})
    entity_id = create.json()["id"]

    response = await admin_ac.delete(f"/admin/entities/{entity_id}")
    assert response.status_code == 200

    response = await admin_ac.get(f"/admin/entities/{entity_id}")
    assert response.status_code == 404