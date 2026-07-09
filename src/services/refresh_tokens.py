from datetime import datetime, timezone, timedelta

from src.config import settings
from src.schemas.refresh_tokens import RefreshTokenAddSchema
from src.services.base import BaseService
from src.utils.exceptions import InvalidTokenError, NoResultFoundException, UserNotFoundException


class RefreshTokensService(BaseService):

    async def create_refresh_token(self, user_id: int, jwt_manager) -> str:
        await self._db.refresh_tokens.delete_by_user_id(user_id)

        token = jwt_manager.create_token(
            payload={"user_id": user_id},
            ttl=settings.REFRESH_TOKEN_TTL_DAYS * 24 * 3600,
        )
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_TTL_DAYS)

        await self._db.refresh_tokens.add_one(RefreshTokenAddSchema(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        ))
        await self._db.commit()
        return token

    async def refresh_access_token(self, refresh_token: str, jwt_manager):
        token_obj = await self._db.refresh_tokens.get_by_token(refresh_token)
        if not token_obj:
            raise InvalidTokenError

        # проверяем что не протух
        if token_obj.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            await self._db.refresh_tokens.delete_by_user_id(token_obj.user_id)
            await self._db.commit()
            raise InvalidTokenError

        try:
            payload = jwt_manager.decode_token(refresh_token)
        except Exception:
            raise InvalidTokenError

        try:
            user = await self._db.users.get_one(id=payload["user_id"])
        except NoResultFoundException:
            raise UserNotFoundException

        try:
            role = await self._db.roles.get_one(id=user.role_id)
        except NoResultFoundException:
            raise InvalidTokenError

        access_token = jwt_manager.create_token({
            "user_id": user.id,
            "role": role.name,
        })
        return access_token

    async def revoke_refresh_token(self, user_id: int):
        await self._db.refresh_tokens.delete_by_user_id(user_id)
        await self._db.commit()