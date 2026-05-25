from dataclasses import dataclass
from decimal import Decimal
import uuid

from sqlalchemy import select

from app.models.marca import Marca
from app.models.modelo import Modelo
from app.repositories.base import BaseRepository, PaginatedResult


@dataclass
class ModelFilters:
    nome: str | None = None
    marca_id: uuid.UUID | None = None


@dataclass
class ModelBrandContext:
    modelo_id: uuid.UUID
    nome: str
    marca: str
    valor_fipe: Decimal


class ModelRepository(BaseRepository[Modelo]):
    model = Modelo

    def get_with_brand(self, model_id: uuid.UUID) -> ModelBrandContext | None:
        stmt = (
            select(
                Modelo.id,
                Modelo.nome,
                Marca.nome_marca,
                Modelo.valor_fipe,
            )
            .join(Marca, Modelo.marca_id == Marca.id)
            .where(
                Modelo.id == model_id,
                Modelo.deleted_at.is_(None),
                Marca.deleted_at.is_(None),
            )
        )
        row = self.db.execute(stmt).one_or_none()
        if row is None:
            return None
        return ModelBrandContext(
            modelo_id=row.id,
            nome=row.nome,
            marca=row.nome_marca,
            valor_fipe=row.valor_fipe,
        )

    def list(
        self,
        *,
        filters: ModelFilters | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedResult[Modelo]:
        stmt = self._active(select(Modelo).order_by(Modelo.nome))

        if filters:
            if filters.nome:
                stmt = stmt.where(Modelo.nome.ilike(f"%{filters.nome}%"))
            if filters.marca_id:
                stmt = stmt.where(Modelo.marca_id == filters.marca_id)

        return self._paginate(stmt, page=page, page_size=page_size)

    def create(
        self,
        *,
        marca_id: uuid.UUID,
        nome: str,
        valor_fipe: object,
        icone: str | None = None,
    ) -> Modelo:
        modelo = Modelo(
            marca_id=marca_id,
            nome=nome,
            valor_fipe=valor_fipe,
            icone=icone,
        )
        self.db.add(modelo)
        return self._commit_refresh(modelo)

    def update(self, modelo: Modelo, **fields: object) -> Modelo:
        for key, value in fields.items():
            setattr(modelo, key, value)
        return self._commit_refresh(modelo)
