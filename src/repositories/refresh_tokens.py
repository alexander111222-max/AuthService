from sqlalchemy import delete

from src.models.refresh_tokens import RefreshTokensOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RefreshTokensDataMapper


class RefreshTokensRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, RefreshTokensOrm)

    mapper = RefreshTokensDataMapper

    async def get_by_token(self, token: str):
        return await self.get_one_or_none(token=token)

    async def delete_by_user_id(self, user_id: int):
        stmt = delete(self._model).filter_by(user_id=user_id).returning(self._model)
        obj = await self._session.execute(stmt)
        return obj.scalar_one_or_none()