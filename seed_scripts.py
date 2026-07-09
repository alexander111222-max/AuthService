import asyncio

from src.database import async_session_maker
from src.models.permissions import ActionEnum, ScopeEnum
from src.schemas.entities import EntityAddSchema
from src.schemas.permissions import PermissionAddSchema
from src.schemas.roles import RoleAddSchema
from src.schemas.users import UserAddSchema
from src.utils.auth import PasswordManager
from src.utils.database import DBManager


async def seed():
    async with DBManager(async_session_maker) as db:


        admin_role = await db.roles.add_one(RoleAddSchema(name="admin", description="Полный доступ ко всему"))
        manager_role = await db.roles.add_one(RoleAddSchema(name="manager", description="Управление товарами и заказами"))
        user_role = await db.roles.add_one(RoleAddSchema(name="user", description="Базовый доступ только на чтение"))


        products = await db.entities.add_one(EntityAddSchema(name="products", description="Товары"))
        orders = await db.entities.add_one(EntityAddSchema(name="orders", description="Заказы"))
        shops = await db.entities.add_one(EntityAddSchema(name="shops", description="Магазины"))

        entities = [products, orders, shops]


        # admin всё и везде
        for entity in entities:
            for action in ActionEnum:
                await db.permissions.add_one(PermissionAddSchema(
                    role_id=admin_role.id,
                    entity_id=entity.id,
                    action=action,
                    scope=ScopeEnum.all,
                ))

        # manager - read all, create all, update own
        for entity in entities:
            for action in [ActionEnum.read, ActionEnum.create]:
                await db.permissions.add_one(PermissionAddSchema(
                    role_id=manager_role.id,
                    entity_id=entity.id,
                    action=action,
                    scope=ScopeEnum.all,
                ))
            await db.permissions.add_one(PermissionAddSchema(
                role_id=manager_role.id,
                entity_id=entity.id,
                action=ActionEnum.update,
                scope=ScopeEnum.own,
            ))

        # user - только read all
        for entity in entities:
            await db.permissions.add_one(PermissionAddSchema(
                role_id=user_role.id,
                entity_id=entity.id,
                action=ActionEnum.read,
                scope=ScopeEnum.all,
            ))


        await db.users.add_one(UserAddSchema(
            first_name="Admin",
            last_name="Admin",
            middle_name="Admin",
            email="admin@admin.com",
            hashed_password=PasswordManager().hash_password("admin123"),
            role_id=admin_role.id,
        ))

        await db.commit()
        print("Seed выполнен успешно")


if __name__ == "__main__":
    asyncio.run(seed())