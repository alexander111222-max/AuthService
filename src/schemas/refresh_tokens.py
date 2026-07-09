from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RefreshTokenAddSchema(BaseModel):
    user_id: int
    token: str
    expires_at: datetime


class RefreshTokenSchema(BaseModel):
    id: int
    user_id: int
    token: str
    expires_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)