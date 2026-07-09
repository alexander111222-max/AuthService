from pydantic import BaseModel, ConfigDict


class EntityAddSchema(BaseModel):
    name: str
    description: str | None = None


class EntityUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None


class EntitySchema(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)