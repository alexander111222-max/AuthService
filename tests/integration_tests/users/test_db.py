from src.schemas.users import UserAddSchema, UserUpdateSchema, UserSoftDeleteSchema
from src.schemas.users import UserSchema
from src.utils.auth import PasswordManager
from src.utils.database import DBManager

password_manager = PasswordManager()


async def test_users_crud(db: DBManager):
    role = await db.roles.get_by_name("user")
    assert role is not None

    new_user: UserSchema = await db.users.add_one(UserAddSchema(
        first_name="Test",
        last_name="User",
        middle_name="Test",
        email="crud_test@test.com",
        hashed_password=password_manager.hash_password("password123"),
        role_id=role.id,
    ))
    await db.commit()

    user: UserSchema | None = await db.users.get_one_or_none(id=new_user.id)
    assert user
    assert user.id == new_user.id
    assert user.email == "crud_test@test.com"
    assert user.first_name == "Test"
    assert user.is_active is True

    updated_user: UserSchema = await db.users.edit(
        UserUpdateSchema(first_name="Updated"),
        id=new_user.id,
    )
    await db.commit()
    assert updated_user.first_name == "Updated"

    deleted_user: UserSchema = await db.users.edit(
        UserSoftDeleteSchema(is_active=False),
        id=new_user.id,
    )
    await db.commit()
    assert deleted_user.is_active is False

    user_in_db: UserSchema | None = await db.users.get_one_or_none(id=new_user.id)
    assert user_in_db
    assert user_in_db.is_active is False


async def test_get_user_by_email(db: DBManager):
    user: UserSchema | None = await db.users.get_by_email("admin@test.com")
    assert user is not None
    assert user.email == "admin@test.com"


async def test_get_user_by_email_not_found(db: DBManager):
    user: UserSchema | None = await db.users.get_by_email("123exist@test.com")
    assert user is None