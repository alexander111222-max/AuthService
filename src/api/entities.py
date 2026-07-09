import logging

from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, AdminDep
from src.schemas.entities import EntityAddSchema, EntityUpdateSchema
from src.services.entities import EntitiesService
from src.utils.exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/entities", tags=["Админ - Сущности"])


@router.post(
    "",
    summary="Создать сущность",
    description="Создаёт новый объект бизнес-приложения для системы прав. Доступно только администратору"
)
async def add_entity(data: EntityAddSchema, db: DBDep, _: AdminDep):
    logger.info(f"Создание сущности: {data.name}")
    try:
        return await EntitiesService(db).add_one(data)
    except EntityAlreadyExistsException:
        logger.warning(f"Сущность уже существует: {data.name}")
        raise HTTPException(status_code=409, detail="Сущность уже существует")


@router.get(
    "",
    summary="Получить все сущности",
    description="Возвращает список всех объектов бизнес-приложения",
)
async def get_all_entities(db: DBDep, _: AdminDep):
    logger.info("Получение всех сущностей")
    return await EntitiesService(db).get_all()


@router.get(
    "/{entity_id}",
    summary="Получить сущность по id"
)
async def get_entity(entity_id: int, db: DBDep, _: AdminDep):
    logger.info(f"Получение сущности с id: {entity_id}")
    try:
        return await EntitiesService(db).get_one(entity_id)
    except EntityNotFoundException:
        raise HTTPException(status_code=404, detail="Сущность не найдена")


@router.patch(
    "/{entity_id}",
    summary="Обновить сущность"
)
async def edit_entity(entity_id: int, data: EntityUpdateSchema, db: DBDep, _: AdminDep):
    logger.info(f"Обновление сущности с id: {entity_id}")
    try:
        return await EntitiesService(db).edit(entity_id, data)
    except EntityNotFoundException:
        raise HTTPException(status_code=404, detail="Сущность не найдена")
    except EntityAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Сущность с таким именем уже существует")


@router.delete(
    "/{entity_id}",
    summary="Удалить сущность"
)
async def delete_entity(entity_id: int, db: DBDep, _: AdminDep):
    logger.info(f"Удаление сущности с id: {entity_id}")
    try:
        return await EntitiesService(db).delete(entity_id)
    except EntityNotFoundException:
        raise HTTPException(status_code=404, detail="Сущность не найдена")