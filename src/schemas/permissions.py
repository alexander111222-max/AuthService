from pydantic import BaseModel, ConfigDict
from src.models.permissions import ActionEnum, ScopeEnum


class PermissionAddSchema(BaseModel):
    role_id: int
    entity_id: int
    action: ActionEnum
    scope: ScopeEnum


class PermissionUpdateSchema(BaseModel):
    action: ActionEnum | None = None
    scope: ScopeEnum | None = None


class PermissionSchema(BaseModel):
    id: int
    role_id: int
    entity_id: int
    action: ActionEnum
    scope: ScopeEnum

    model_config = ConfigDict(from_attributes=True)