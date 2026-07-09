from httpx import AsyncClient


async def test_get_all_permissions(admin_ac: AsyncClient):
    response = await admin_ac.get("/admin/permissions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


async def test_get_all_permissions_forbidden(user_ac: AsyncClient):
    response = await user_ac.get("/admin/permissions")
    assert response.status_code == 403


async def test_get_permissions_by_role(admin_ac: AsyncClient):
    roles = await admin_ac.get("/admin/roles")
    admin_role = next(r for r in roles.json() if r["name"] == "admin")

    response = await admin_ac.get(f"/admin/permissions/role/{admin_role['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


async def test_get_permissions_by_role_not_found(admin_ac: AsyncClient):
    response = await admin_ac.get("/admin/permissions/role/99999")
    assert response.status_code == 404


async def test_delete_permission(admin_ac: AsyncClient):
    permissions = await admin_ac.get("/admin/permissions")
    permission_id = permissions.json()[0]["id"]

    response = await admin_ac.delete(f"/admin/permissions/{permission_id}")
    assert response.status_code == 200

    response = await admin_ac.get("/admin/permissions")
    ids = [p["id"] for p in response.json()]
    assert permission_id not in ids