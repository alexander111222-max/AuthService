from sqlalchemy import select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UsersDataMapper, UsersWithPasswordDataMapper


class UsersRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, UsersOrm)

    mapper = UsersDataMapper

    async def get_by_email(self, email: str):
        query = select(self._model).filter_by(email=email)
        obj = await self._session.execute(query)
        result = obj.scalar_one_or_none()
        if result is None:
            return None
        return UsersWithPasswordDataMapper.map_to_domain_entity(result)