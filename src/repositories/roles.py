from src.models.roles import RolesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RolesDataMapper


class RolesRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, RolesOrm)

    mapper = RolesDataMapper

    async def get_by_name(self, name: str):
        return await self.get_one_or_none(name=name)