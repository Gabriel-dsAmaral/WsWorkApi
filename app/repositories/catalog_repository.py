from dataclasses import dataclass
import uuid
from decimal import Decimal

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.models.marca import Marca
from app.models.modelo import Modelo


@dataclass
class CatalogModelRow:
    id: uuid.UUID
    nome: str
    marca: str
    valor_fipe: Decimal


class CatalogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_models(self) -> list[CatalogModelRow]:
        stmt = (
            select(
                Modelo.id,
                Modelo.nome,
                Marca.nome_marca.label("marca"),
                Modelo.valor_fipe,
            )
            .join(Marca, Modelo.marca_id == Marca.id)
            .where(
                Modelo.deleted_at.is_(None),
                Marca.deleted_at.is_(None),
            )
            .order_by(Marca.nome_marca, Modelo.nome)
        )
        rows = self.db.execute(stmt).all()
        return [
            CatalogModelRow(
                id=row.id,
                nome=row.nome,
                marca=row.marca,
                valor_fipe=row.valor_fipe,
            )
            for row in rows
        ]
