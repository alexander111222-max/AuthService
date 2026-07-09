import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator, Any

from src.api.dependencies import get_db
from src.config import settings
from src.database import engine_null_pool, Base, async_session_maker_null_pool
from src.main import app
from src.utils.database import DBManager

transport = ASGITransport(app=app)


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def db(setup_database) -> AsyncGenerator:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def fill_database(setup_database):
    from src.models.permissions import ActionEnum, ScopeEnum
    from src.schemas.entities import EntityAddSchema
    from src.schemas.permissions import PermissionAddSchema
    from src.schemas.roles import RoleAddSchema
    from src.schemas.users import UserAddSchema
    from src.utils.auth import PasswordManager

    password_manager = PasswordManager()

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        admin_role = await db.roles.add_one(RoleAddSchema(name="admin", description="Полный доступ"))
        manager_role = await db.roles.add_one(RoleAddSchema(name="manager", description="Управление"))
        user_role = await db.roles.add_one(RoleAddSchema(name="user", description="Базовый доступ"))

        products = await db.entities.add_one(EntityAddSchema(name="products", description="Товары"))
        orders = await db.entities.add_one(EntityAddSchema(name="orders", description="Заказы"))
        shops = await db.entities.add_one(EntityAddSchema(name="shops", description="Магазины"))

        entities = [products, orders, shops]

        # права admin
        for entity in entities:
            for action in ActionEnum:
                await db.permissions.add_one(PermissionAddSchema(
                    role_id=admin_role.id, entity_id=entity.id,
                    action=action, scope=ScopeEnum.all,
                ))

        # права manager
        for entity in entities:
            for action in [ActionEnum.read, ActionEnum.create]:
                await db.permissions.add_one(PermissionAddSchema(
                    role_id=manager_role.id, entity_id=entity.id,
                    action=action, scope=ScopeEnum.all,
                ))
            await db.permissions.add_one(PermissionAddSchema(
                role_id=manager_role.id, entity_id=entity.id,
                action=ActionEnum.update, scope=ScopeEnum.own,
            ))

        # права user
        for entity in entities:
            await db.permissions.add_one(PermissionAddSchema(
                role_id=user_role.id, entity_id=entity.id,
                action=ActionEnum.read, scope=ScopeEnum.all,
            ))

        # создаём юзеров
        await db.users.add_one(UserAddSchema(
            first_name="Admin", last_name="System", middle_name="Admin",
            email="admin@test.com",
            hashed_password=password_manager.hash_password("admin123"),
            role_id=admin_role.id,
        ))
        await db.users.add_one(UserAddSchema(
            first_name="Manager", last_name="System", middle_name="Manager",
            email="manager@test.com",
            hashed_password=password_manager.hash_password("manager123"),
            role_id=manager_role.id,
        ))
        await db.users.add_one(UserAddSchema(
            first_name="User", last_name="System", middle_name="User",
            email="user@test.com",
            hashed_password=password_manager.hash_password("user123"),
            role_id=user_role.id,
        ))

        await db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[Any, Any]:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def get_authenticated_client(ac: AsyncClient, email: str, password: str) -> AsyncClient:
    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    ac.cookies.set("access_token", response.cookies.get("access_token"))
    return ac


@pytest.fixture(scope="session")
async def admin_ac(ac, fill_database) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", json={"email": "admin@test.com", "password": "admin123"})
        assert response.status_code == 200
        client.cookies.set("access_token", response.cookies.get("access_token"))
        yield client


@pytest.fixture(scope="session")
async def manager_ac(ac, fill_database) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", json={"email": "manager@test.com", "password": "manager123"})
        assert response.status_code == 200
        client.cookies.set("access_token", response.cookies.get("access_token"))
        yield client


@pytest.fixture(scope="session")
async def user_ac(ac, fill_database) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", json={"email": "user@test.com", "password": "user123"})
        assert response.status_code == 200
        client.cookies.set("access_token", response.cookies.get("access_token"))
        yield client