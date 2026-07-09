import logging

from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from src.api.dependencies import AdminDep
from src.schemas.users import UserChangeRoleSchema
from src.services.refresh_tokens import RefreshTokensService
from src.utils.exceptions import RoleNotFoundException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.users import UserUpdateSchema
from src.services.users import UsersService
from src.utils.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get(
    "/me",
    summary="Получить свой профиль",
    description="Возвращает данные текущего авторизованного пользователя"
)
async def get_me(db: DBDep, user_id: UserIdDep):
    logger.info(f"Получение профиля пользователя с id: {user_id}")
    try:
        return await UsersService(db).get_one(user_id)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.patch(
    "/me",
    summary="Обновить свой профиль",
    description="Обновляет данные текущего пользователя. Все поля опциональны"
)
async def edit_me(data: UserUpdateSchema, db: DBDep, user_id: UserIdDep):
    logger.info(f"Обновление профиля пользователя с id: {user_id}")
    try:
        return await UsersService(db).edit(user_id, data)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    except UserAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Email уже занят")


@router.delete(
    "/me",
    summary="Удалить свой аккаунт",
    description=" удаление - аккаунт деактивируется, пользователь разлогинивается"
)
async def delete_me(response: Response, db: DBDep, user_id: UserIdDep):
    try:
        await UsersService(db).delete(user_id)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    await RefreshTokensService(db).revoke_refresh_token(user_id)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"status": "ok"}



@router.patch(
    "/admin/{user_id}/role",
    summary="Изменить роль пользователя",
    description="Доступно только администратору. Меняет роль любого пользователя"
)
async def change_user_role(user_id: int, data: UserChangeRoleSchema, db: DBDep, _: AdminDep):
    logger.info(f"Смена роли пользователя с id: {user_id} на role_id: {data.role_id}")
    try:
        return await UsersService(db).change_role(user_id, data.role_id)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    except RoleNotFoundException:
        raise HTTPException(status_code=404, detail="Роль не найдена")