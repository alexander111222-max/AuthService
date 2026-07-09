from src.schemas.entities import EntityAddSchema, EntityUpdateSchema
from src.services.base import BaseService
from src.utils.exceptions import (
    NoResultFoundException,
    ObjectAlreadyExistsException,
    EntityNotFoundException,
    EntityAlreadyExistsException,
)


class EntitiesService(BaseService):

    async def add_one(self, data: EntityAddSchema):
        try:
            entity = await self._db.entities.add_one(data)
        except ObjectAlreadyExistsException:
            raise EntityAlreadyExistsException
        await self._db.commit()
        return entity

    async def get_all(self):
        return await self._db.entities.get_all()

    async def get_one(self, entity_id: int):
        try:
            return await self._db.entities.get_one(id=entity_id)
        except NoResultFoundException:
            raise EntityNotFoundException

    async def edit(self, entity_id: int, data: EntityUpdateSchema):
        try:
            entity = await self._db.entities.edit(data, id=entity_id)
        except NoResultFoundException:
            raise EntityNotFoundException
        except ObjectAlreadyExistsException:
            raise EntityAlreadyExistsException
        await self._db.commit()
        return entity

    async def delete(self, entity_id: int):
        try:
            entity = await self._db.entities.delete(id=entity_id)
        except NoResultFoundException:
            raise EntityNotFoundException
        await self._db.commit()
        return entity