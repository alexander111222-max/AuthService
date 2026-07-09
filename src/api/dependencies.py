from typing import Annotated

from starlette.requests import Request
from fastapi import HTTPException, Depends

from src.utils.exceptions import EntityNotFoundException, RoleNotFoundException
from src.config import settings
from src.database import async_session_maker
from src.models.permissions import ActionEnum
from src.services.permissions import PermissionsService
from src.utils.auth import PasswordManager, JWTManager
from src.utils.database import DBManager
from src.utils.exceptions import TokenExpiredError, InvalidTokenError


async def get_db():
    async with DBManager(async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


PassManagerDep = Annotated[PasswordManager, Depends(PasswordManager)]

jwt_manager = JWTManager(secret=settings.SECRET_KEY)

def get_jwt_manager() -> JWTManager:
    return jwt_manager

JWTManagerDep = Annotated[JWTManager, Depends(get_jwt_manager)]



def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Сначала авторизуйтесь")
    return token


def get_current_payload(token: str = Depends(get_token)) -> dict:
    try:
        payload = jwt_manager.decode_token(token)
    except TokenExpiredError:
        raise HTTPException(status_code=401, detail="Токен истёк, авторизуйтесь снова")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Не валидный токен")
    return payload


def get_current_user_id(payload: dict = Depends(get_current_payload)) -> int:
    return payload["user_id"]


def require_admin(payload: dict = Depends(get_current_payload)) -> dict:
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return payload


PayloadDep = Annotated[dict, Depends(get_current_payload)]
UserIdDep = Annotated[int, Depends(get_current_user_id)]
AdminDep = Annotated[dict, Depends(require_admin)]



def check_permission(entity_name: str, action: ActionEnum):
    async def dependency(payload: PayloadDep, db: DBDep):
        try:
            permission = await PermissionsService(db).get_permission(
                role=payload["role"],
                entity_name=entity_name,
                action=action,
            )
        except EntityNotFoundException:
            raise HTTPException(status_code=404, detail="Сущность не найдена")
        except RoleNotFoundException:
            raise HTTPException(status_code=404, detail="Роль не найдена")

        if permission is None:
            raise HTTPException(status_code=403, detail="Доступ запрещён")

        return permission.scope

    return dependency
















