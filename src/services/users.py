from src.schemas.users import UserRegisterSchema, UserUpdateSchema, UserAddSchema, UserSoftDeleteSchema, \
    UserChangeRoleSchema
from src.services.base import BaseService
from src.utils.exceptions import (
    NoResultFoundException,
    ObjectAlreadyExistsException,
    UserNotFoundException,
    UserAlreadyExistsException,
    UserNotActiveException,
    WrongPasswordException,
    RoleNotFoundException,
)


class UsersService(BaseService):

    async def register(self, data: UserRegisterSchema, password_manager):
        if data.password != data.password_confirm:
            raise WrongPasswordException

        role = await self._db.roles.get_by_name("user")
        if not role:
            raise RoleNotFoundException

        existing = await self._db.users.get_by_email(data.email)
        if existing:
            raise UserAlreadyExistsException

        hashed_password = password_manager.hash_password(data.password)

        user = await self._db.users.add_one(UserAddSchema(
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            email=data.email,
            hashed_password=hashed_password,
            role_id=role.id,
        ))
        await self._db.commit()
        return user

    async def get_one(self, user_id: int):
        try:
            return await self._db.users.get_one(id=user_id)
        except NoResultFoundException:
            raise UserNotFoundException

    async def get_all(self):
        return await self._db.users.get_all()

    async def edit(self, user_id: int, data: UserUpdateSchema):
        try:
            user = await self._db.users.edit(data, id=user_id)
        except NoResultFoundException:
            raise UserNotFoundException
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException
        await self._db.commit()
        return user

    async def delete(self, user_id: int):
        try:
            await self._db.users.get_one(id=user_id)
        except NoResultFoundException:
            raise UserNotFoundException

        user = await self._db.users.edit(UserSoftDeleteSchema(is_active=False), id=user_id)
        await self._db.commit()
        return user

    async def login(self, email: str, password: str, password_manager, jwt_manager):
        user = await self._db.users.get_by_email(email)
        if not user:
            raise UserNotFoundException

        if not user.is_active:
            raise UserNotActiveException

        if not password_manager.verify_password(password, user.hashed_password):
            raise WrongPasswordException

        role = await self._db.roles.get_one(id=user.role_id)
        token = jwt_manager.create_token({"user_id": user.id, "role": role.name})
        return token

    async def change_role(self, user_id: int, role_id: int):
        try:
            await self._db.users.get_one(id=user_id)
        except NoResultFoundException:
            raise UserNotFoundException

        try:
            await self._db.roles.get_one(id=role_id)
        except NoResultFoundException:
            raise RoleNotFoundException

        user = await self._db.users.edit(UserChangeRoleSchema(role_id=role_id), id=user_id)
        await self._db.commit()
        return user