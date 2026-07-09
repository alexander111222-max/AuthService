from src.schemas.roles import RoleSchema
from src.utils.database import DBManager


async def test_get_all_roles(db: DBManager):
    roles = await db.roles.get_all()
    assert len(roles) >= 3


async def test_get_role_by_id(db: DBManager):
    roles = await db.roles.get_all()
    role_id = roles[0].id
    role: RoleSchema | None = await db.roles.get_one_or_none(id=role_id)
    assert role
    assert role.id == role_id


async def test_get_role_by_name(db: DBManager):
    role: RoleSchema | None = await db.roles.get_by_name("admin")
    assert role is not None
    assert role.name == "admin"


async def test_get_role_by_name_manager(db: DBManager):
    role: RoleSchema | None = await db.roles.get_by_name("manager")
    assert role is not None
    assert role.name == "manager"


async def test_get_role_by_name_user(db: DBManager):
    role: RoleSchema | None = await db.roles.get_by_name("user")
    assert role is not None
    assert role.name == "user"