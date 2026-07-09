from src.models.permissions import ActionEnum, ScopeEnum
from src.schemas.permissions import PermissionAddSchema, PermissionSchema, PermissionUpdateSchema
from src.utils.database import DBManager


async def test_permissions_crud(db: DBManager):
    role = await db.roles.get_by_name("user")
    entity = await db.entities.get_by_name("products")

    new_permission: PermissionSchema = await db.permissions.add_one(PermissionAddSchema(
        role_id=role.id,
        entity_id=entity.id,
        action=ActionEnum.delete,
        scope=ScopeEnum.own,
    ))
    await db.commit()

    permission: PermissionSchema | None = await db.permissions.get_one_or_none(id=new_permission.id)
    assert permission
    assert permission.role_id == role.id
    assert permission.entity_id == entity.id
    assert permission.action == ActionEnum.delete
    assert permission.scope == ScopeEnum.own

    updated: PermissionSchema = await db.permissions.edit(
        PermissionUpdateSchema(scope=ScopeEnum.all),
        id=new_permission.id,
    )
    await db.commit()
    assert updated.scope == ScopeEnum.all

    await db.permissions.delete(id=new_permission.id)
    await db.commit()

    deleted: PermissionSchema | None = await db.permissions.get_one_or_none(id=new_permission.id)
    assert not deleted


async def test_get_role_permissions(db: DBManager):
    role = await db.roles.get_by_name("admin")
    permissions = await db.permissions.get_role_permissions(role.id)
    assert len(permissions) > 0



async def test_get_one_permission_not_found(db: DBManager):
    role = await db.roles.get_by_name("user")
    entity = await db.entities.get_by_name("products")

    permission = await db.permissions.get_one_permission(
        role_id=role.id,
        entity_id=entity.id,
        action=ActionEnum.delete,
    )
    assert permission is None