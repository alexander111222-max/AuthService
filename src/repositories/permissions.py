
from src.models.permissions import PermissionsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import PermissionsDataMapper


class PermissionsRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, PermissionsOrm)

    mapper = PermissionsDataMapper

    async def get_role_permissions(self, role_id: int):
        return await self.get_filter_by(role_id=role_id)

    async def get_one_permission(self, role_id: int, entity_id: int, action: str):
        return await self.get_one_or_none(role_id=role_id, entity_id=entity_id, action=action)