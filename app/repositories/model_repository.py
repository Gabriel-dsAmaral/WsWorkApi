from dataclasses import dataclass
import uuid

from sqlalchemy import select

from app.models.modelo import Modelo
from app.repositories.base import BaseRepository, PaginatedResult


@dataclass
class ModelFilters:
    nome: str | None = None
    marca_id: uuid.UUID | None = None


class ModelRepository(BaseRepository[Modelo]):
    model = Modelo

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
