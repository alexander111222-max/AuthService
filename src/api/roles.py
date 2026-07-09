import logging

from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, AdminDep
from src.schemas.roles import RoleAddSchema
from src.services.roles import RolesService
from src.utils.exceptions import (
    RoleNotFoundException,
    RoleAlreadyExistsException,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/roles", tags=["Админ - Роли"])


@router.post(
    "",
    summary="Создать роль",
    description="Создаёт новую роль. Доступно только администратору"
)
async def add_role(data: RoleAddSchema, db: DBDep, _: AdminDep):
    logger.info(f"Создание роли: {data.name}")
    try:
        role = await RolesService(db).add_one(data)
    except RoleAlreadyExistsException:
        logger.warning(f"Роль уже существует: {data.name}")
        raise HTTPException(status_code=409, detail="Роль уже существует")
    return role


@router.get(
    "",
    summary="Получить все роли",
    description="Возвращает список всех ролей. Доступно только администратору",
)
async def get_all_roles(db: DBDep, _: AdminDep):
    logger.info("Получение всех ролей")
    return await RolesService(db).get_all()


@router.get(
    "/{role_id}",
    summary="Получить роль по id"
)
async def get_role(role_id: int, db: DBDep, _: AdminDep):
    logger.info(f"Получение роли с id: {role_id}")
    try:
        return await RolesService(db).get_one(role_id)
    except RoleNotFoundException:
        raise HTTPException(status_code=404, detail="Роль не найдена")


@router.delete(
    "/{role_id}",
    summary="Удалить роль"
)
async def delete_role(role_id: int, db: DBDep, _: AdminDep):
    logger.info(f"Удаление роли с id: {role_id}")
    try:
        return await RolesService(db).delete(role_id)
    except RoleNotFoundException:
        raise HTTPException(status_code=404, detail="Роль не найдена")