import enum
import typing

from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.permissions import PermissionsOrm
    from src.models import UsersOrm


class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class RolesOrm(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[RoleEnum] = mapped_column(unique=True)
    description: Mapped[str | None]

    users: Mapped[list["UsersOrm"]] = relationship(back_populates="role")
    permissions: Mapped[list["PermissionsOrm"]] = relationship(back_populates="role")


