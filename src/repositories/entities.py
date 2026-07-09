from src.models.entities import EntitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import EntitiesDataMapper


class EntitiesRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, EntitiesOrm)

    mapper = EntitiesDataMapper

    async def get_by_name(self, name: str):
        return await self.get_one_or_none(name=name)