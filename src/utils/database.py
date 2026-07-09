from src.repositories.entities import EntitiesRepository
from src.repositories.permissions import PermissionsRepository
from src.repositories.refresh_tokens import RefreshTokensRepository
from src.repositories.roles import RolesRepository
from src.repositories.users import UsersRepository


class DBManager:

    def __init__(self, session_factory):
        self._session_factory = session_factory


    async def __aenter__(self):
        self._session = self._session_factory()

        self.users = UsersRepository(self._session)
        self.entities = EntitiesRepository(self._session)
        self.permissions = PermissionsRepository(self._session)
        self.roles = RolesRepository(self._session)
        self.refresh_tokens = RefreshTokensRepository(self._session)



        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.rollback()
        await self._session.close()

    async def commit(self):
        await self._session.commit()
