from src.models import UsersOrm, RolesOrm, EntitiesOrm, PermissionsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.entities import EntitySchema
from src.schemas.permissions import PermissionSchema
from src.schemas.roles import RoleSchema
from src.schemas.users import UserSchema
from src.models.refresh_tokens import RefreshTokensOrm
from src.schemas.refresh_tokens import RefreshTokenSchema
from src.schemas.users import UserWithPasswordSchema

class UsersDataMapper(DataMapper[UsersOrm, UserSchema]):
    schema = UserSchema
    model = UsersOrm

class RolesDataMapper(DataMapper[RolesOrm, RoleSchema]):
    schema = RoleSchema
    model = RolesOrm


class EntitiesDataMapper(DataMapper[EntitiesOrm, EntitySchema]):
    schema = EntitySchema
    model = EntitiesOrm


class PermissionsDataMapper(DataMapper[PermissionsOrm, PermissionSchema]):
    schema = PermissionSchema
    model = PermissionsOrm



class RefreshTokensDataMapper(DataMapper[RefreshTokensOrm, RefreshTokenSchema]):
    schema = RefreshTokenSchema
    model = RefreshTokensOrm


class UsersWithPasswordDataMapper(DataMapper[UsersOrm, UserWithPasswordSchema]):
    schema = UserWithPasswordSchema
    model = UsersOrm