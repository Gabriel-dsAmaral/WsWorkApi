from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.modelo import Modelo


class Marca(BaseModel):
    __tablename__ = "marcas"

    nome_marca: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    icone: Mapped[str | None] = mapped_column(String(512), nullable=True)

    modelos: Mapped[list[Modelo]] = relationship(
        back_populates="marca",
        cascade="all, delete-orphan",
    )
