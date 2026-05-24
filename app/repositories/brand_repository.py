from dataclasses import dataclass

from sqlalchemy import select

from app.models.marca import Marca
from app.repositories.base import BaseRepository, PaginatedResult


@dataclass
class BrandFilters:
    nome_marca: str | None = None


class BrandRepository(BaseRepository[Marca]):
    model = Marca

    def get_by_name(self, nome_marca: str) -> Marca | None:
        stmt = self._active(select(Marca)).where(Marca.nome_marca == nome_marca)
        return self.db.scalars(stmt).first()

    def list(
        self,
        *,
        filters: BrandFilters | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedResult[Marca]:
        stmt = self._active(select(Marca).order_by(Marca.nome_marca))

        if filters and filters.nome_marca:
            stmt = stmt.where(Marca.nome_marca.ilike(f"%{filters.nome_marca}%"))

        return self._paginate(stmt, page=page, page_size=page_size)

    def create(self, *, nome_marca: str, icone: str | None = None) -> Marca:
        marca = Marca(nome_marca=nome_marca, icone=icone)
        self.db.add(marca)
        return self._commit_refresh(marca)

    def update(self, marca: Marca, **fields: object) -> Marca:
        for key, value in fields.items():
            setattr(marca, key, value)
        return self._commit_refresh(marca)
