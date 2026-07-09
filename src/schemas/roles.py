from src.models.roles import RoleEnum
from pydantic import BaseModel, ConfigDict


class RoleAddSchema(BaseModel):
    name: RoleEnum
    description: str | None = None


class RoleSchema(BaseModel):
    id: int
    name: RoleEnum
    description: str | None

    model_config = ConfigDict(from_attributes=True)