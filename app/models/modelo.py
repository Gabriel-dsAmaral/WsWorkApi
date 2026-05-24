from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.types import uuid_fk
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.carro import Carro
    from app.models.marca import Marca


class Modelo(BaseModel):
    __tablename__ = "modelos"

    marca_id: Mapped[uuid.UUID] = uuid_fk("marcas.id", index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    valor_fipe: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    icone: Mapped[str | None] = mapped_column(String(512), nullable=True)

    marca: Mapped[Marca] = relationship(back_populates="modelos")
    carros: Mapped[list[Carro]] = relationship(
        back_populates="modelo",
        cascade="all, delete-orphan",
    )
