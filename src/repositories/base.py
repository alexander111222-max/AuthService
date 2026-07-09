from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.exc import IntegrityError, DataError, MultipleResultsFound, NoResultFound

from src.repositories.mappers.base import DataMapper
from src.utils.exceptions import (
    MultipleResultsFoundException,
    NoResultFoundException,
    ObjectAlreadyExistsException,
)
from sqlalchemy.exc import IntegrityError


class BaseRepository:

    mapper: type[DataMapper]

    def __init__(self, session, model):
        self._session = session
        self._model = model

    async def add_one(self, data: BaseModel):
        try:
            stmt = insert(self._model).values(**data.model_dump()).returning(self._model)
            obj = await self._session.execute(stmt)
            result = obj.scalar_one()
            return self.mapper.map_to_domain_entity(result)
        except IntegrityError:
            raise ObjectAlreadyExistsException
        except MultipleResultsFound:
            raise MultipleResultsFoundException
        except NoResultFound:
            raise NoResultFoundException

    async def get_all(self):
        query = select(self._model)
        objs = await self._session.execute(query)
        return [self.mapper.map_to_domain_entity(obj) for obj in objs.scalars().all()]

    async def get_filter_by(self, *filters, **filter_by):
        query = select(self._model).filter(*filters).filter_by(**filter_by)
        objs = await self._session.execute(query)
        return [self.mapper.map_to_domain_entity(obj) for obj in objs.scalars().all()]

    async def get_one(self, **filter_by):
        query = select(self._model).filter_by(**filter_by)
        obj = await self._session.execute(query)
        try:
            result = obj.scalar_one()
        except NoResultFound:
            raise NoResultFoundException
        except MultipleResultsFound:
            raise MultipleResultsFoundException
        return self.mapper.map_to_domain_entity(result)

    async def get_one_or_none(self, **filter_by):
        try:
            query = select(self._model).filter_by(**filter_by)
            obj = await self._session.execute(query)
            result = obj.scalar_one_or_none()
            if result is None:
                return None
            return self.mapper.map_to_domain_entity(result)
        except DataError:
            return None

    async def edit(self, data: BaseModel, **filter_by):
        try:
            stmt = (
                update(self._model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=True))
                .returning(self._model)
            )
            obj = await self._session.execute(stmt)
            result = obj.scalar_one()
            return self.mapper.map_to_domain_entity(result)
        except NoResultFound:
            raise NoResultFoundException
        except IntegrityError:
            raise ObjectAlreadyExistsException
        except DataError:
            raise NoResultFoundException

    async def delete(self, **filter_by):
        try:
            stmt = delete(self._model).filter_by(**filter_by).returning(self._model)
            obj = await self._session.execute(stmt)
            result = obj.scalar_one_or_none()
            if result is None:
                raise NoResultFoundException
            return self.mapper.map_to_domain_entity(result)
        except DataError:
            raise NoResultFoundException