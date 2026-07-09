import enum
import typing

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.database import Base
if typing.TYPE_CHECKING:

    from src.models import EntitiesOrm
    from src.models import RolesOrm




class ActionEnum(str, enum.Enum):
    read = "read"
    create = "create"
    update = "update"
    delete = "delete"


class ScopeEnum(str, enum.Enum):
    own = "own"
    all = "all"

class PermissionsOrm(Base):
    __tablename__ = "permissions"

    __table_args__ = (
        UniqueConstraint("role_id", "entity_id", "action", "scope", name="uq_permission"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    entity_id: Mapped[int] = mapped_column(ForeignKey("entities.id", ondelete="CASCADE"))
    action: Mapped[ActionEnum]
    scope: Mapped[ScopeEnum]

    role: Mapped["RolesOrm"] = relationship(back_populates="permissions")
    entity: Mapped["EntitiesOrm"] = relationship(back_populates="permissions")