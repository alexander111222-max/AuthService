
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UserRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    email: EmailStr
    password: str
    password_confirm: str

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

class UserAddSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    email: str
    hashed_password: str
    role_id: int


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    email: EmailStr | None = None


class UserSoftDeleteSchema(BaseModel):
    is_active: bool = False


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    email: str
    is_active: bool
    role_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserChangeRoleSchema(BaseModel):
    role_id: int

class UserWithPasswordSchema(BaseModel):
    id: int
    email: str
    hashed_password: str
    is_active: bool
    role_id: int

    model_config = ConfigDict(from_attributes=True)