import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.permissions import PermissionsOrm


class EntitiesOrm(Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]

    permissions: Mapped[list["PermissionsOrm"]] = relationship(back_populates="entity")
