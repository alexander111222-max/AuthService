from src.schemas.roles import RoleAddSchema
from src.services.base import BaseService
from src.utils.exceptions import (
    NoResultFoundException,
    ObjectAlreadyExistsException,
    RoleNotFoundException,
    RoleAlreadyExistsException,
)


class RolesService(BaseService):

    async def add_one(self, data: RoleAddSchema):
        try:
            role = await self._db.roles.add_one(data)
        except ObjectAlreadyExistsException:
            raise RoleAlreadyExistsException
        await self._db.commit()
        return role

    async def get_all(self):
        return await self._db.roles.get_all()

    async def get_one(self, role_id: int):
        try:
            return await self._db.roles.get_one(id=role_id)
        except NoResultFoundException:
            raise RoleNotFoundException

    async def delete(self, role_id: int):
        try:
            role = await self._db.roles.delete(id=role_id)
        except NoResultFoundException:
            raise RoleNotFoundException
        await self._db.commit()
        return role