from pydantic import BaseModel
from typing_extensions import TypeVar, Generic

from src.database import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper(Generic[ModelType, SchemaType]):
    schema: type[SchemaType]
    model: type[ModelType]

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.model(**data.model_dump())

