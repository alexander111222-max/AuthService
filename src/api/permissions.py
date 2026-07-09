import logging

from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, AdminDep
from src.schemas.permissions import PermissionAddSchema, PermissionUpdateSchema
from src.services.permissions import PermissionsService
from src.utils.exceptions import (
    PermissionNotFoundException,
    PermissionAlreadyExistsException,
    RoleNotFoundException,
    EntityNotFoundException,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/permissions", tags=["Админ - Права доступа"])


@router.post(
    "",
    summary="Создать право доступа",
    description="Назначает право доступа роли к определённой сущности с указанием действия и области"
)
async def add_permission(data: PermissionAddSchema, db: DBDep, _: AdminDep):
    logger.info(f"Создание права: role_id={data.role_id} entity_id={data.entity_id} action={data.action} scope={data.scope}")
    try:
        return await PermissionsService(db).add_one(data)
    except RoleNotFoundException:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    except EntityNotFoundException:
        raise HTTPException(status_code=404, detail="Сущность не найдена")
    except PermissionAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Такое право доступа уже существует")


@router.get(
    "",
    summary="Получить все права доступа",
    description="Возвращает список всех прав доступа в системе",
)
async def get_all_permissions(db: DBDep, _: AdminDep):
    logger.info("Получение всех прав доступа")
    return await PermissionsService(db).get_all()


@router.get(
    "/role/{role_id}",
    summary="Получить права роли",
    description="Возвращает все права доступа для указанной роли"
)
async def get_permissions_by_role(role_id: int, db: DBDep, _: AdminDep):
    logger.info(f"Получение прав для роли с id: {role_id}")
    try:
        return await PermissionsService(db).get_by_role(role_id)
    except RoleNotFoundException:
        raise HTTPException(status_code=404, detail="Роль не найдена")


@router.patch(
    "/{permission_id}",
    summary="Обновить право доступа"
)
async def edit_permission(permission_id: int, data: PermissionUpdateSchema, db: DBDep, _: AdminDep):
    logger.info(f"Обновление права с id: {permission_id}")
    try:
        return await PermissionsService(db).edit(permission_id, data)
    except PermissionNotFoundException:
        raise HTTPException(status_code=404, detail="Право доступа не найдено")


@router.delete(
    "/{permission_id}",
    summary="Удалить право доступа"
)
async def delete_permission(permission_id: int, db: DBDep, _: AdminDep):
    logger.info(f"Удаление права с id: {permission_id}")
    try:
        return await PermissionsService(db).delete(permission_id)
    except PermissionNotFoundException:
        raise HTTPException(status_code=404, detail="Право доступа не найдено")