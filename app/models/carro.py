from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.types import uuid_fk
from app.models.base import BaseModel
from app.models.combustivel import Combustivel

if TYPE_CHECKING:
    from app.models.modelo import Modelo
    from app.models.usuario import Usuario


class Carro(BaseModel):
    __tablename__ = "carros"

    modelo_id: Mapped[uuid.UUID] = uuid_fk("modelos.id", index=True)
    usuario_id: Mapped[uuid.UUID] = uuid_fk("usuarios.id", index=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    combustivel: Mapped[Combustivel] = mapped_column(
        Enum(Combustivel, name="combustivel_enum", native_enum=True),
        nullable=False,
    )
    num_portas: Mapped[int] = mapped_column(Integer, nullable=False)
    cor: Mapped[str] = mapped_column(String(100), nullable=False)
    quilometragem: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_anuncio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    modelo: Mapped[Modelo] = relationship(back_populates="carros")
    usuario: Mapped[Usuario] = relationship(back_populates="carros")
