from src.models.permissions import ActionEnum
from src.schemas.permissions import PermissionAddSchema, PermissionUpdateSchema
from src.services.base import BaseService
from src.utils.exceptions import (
    NoResultFoundException,
    ObjectAlreadyExistsException,
    PermissionNotFoundException,
    PermissionAlreadyExistsException,
    RoleNotFoundException,
    EntityNotFoundException,
)


class PermissionsService(BaseService):

    async def add_one(self, data: PermissionAddSchema):
        try:
            await self._db.roles.get_one(id=data.role_id)
        except NoResultFoundException:
            raise RoleNotFoundException

        try:
            await self._db.entities.get_one(id=data.entity_id)
        except NoResultFoundException:
            raise EntityNotFoundException

        try:
            permission = await self._db.permissions.add_one(data)
        except ObjectAlreadyExistsException:
            raise PermissionAlreadyExistsException
        await self._db.commit()
        return permission

    async def get_all(self):
        return await self._db.permissions.get_all()

    async def get_by_role(self, role_id: int):
        try:
            await self._db.roles.get_one(id=role_id)
        except NoResultFoundException:
            raise RoleNotFoundException
        return await self._db.permissions.get_role_permissions(role_id)

    async def edit(self, permission_id: int, data: PermissionUpdateSchema):
        try:
            permission = await self._db.permissions.edit(data, id=permission_id)
        except NoResultFoundException:
            raise PermissionNotFoundException
        await self._db.commit()
        return permission

    async def delete(self, permission_id: int):
        try:
            permission = await self._db.permissions.delete(id=permission_id)
        except NoResultFoundException:
            raise PermissionNotFoundException
        await self._db.commit()
        return permission

    async def get_permission(self, role: str, entity_name: str, action: ActionEnum):
        try:
            entity = await self._db.entities.get_by_name(entity_name)
        except NoResultFoundException:
            raise EntityNotFoundException

        role_obj = await self._db.roles.get_by_name(role)
        if not role_obj:
            raise RoleNotFoundException

        return await self._db.permissions.get_one_permission(
            role_id=role_obj.id,
            entity_id=entity.id,
            action=action,
        )