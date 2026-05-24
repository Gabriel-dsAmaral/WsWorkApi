from dataclasses import dataclass
import uuid

from sqlalchemy import select

from app.models.carro import Carro
from app.models.combustivel import Combustivel
from app.models.marca import Marca
from app.models.modelo import Modelo
from app.repositories.base import BaseRepository, PaginatedResult


@dataclass
class CarFilters:
    usuario_id: uuid.UUID | None = None
    marca_id: uuid.UUID | None = None
    modelo_id: uuid.UUID | None = None
    ano: int | None = None
    combustivel: Combustivel | None = None


class CarRepository(BaseRepository[Carro]):
    model = Carro

    def list(
        self,
        *,
        filters: CarFilters | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedResult[Carro]:
        stmt = select(Carro).where(Carro.deleted_at.is_(None))

        if filters and filters.marca_id:
            stmt = (
                stmt.join(Modelo, Carro.modelo_id == Modelo.id)
                .join(Marca, Modelo.marca_id == Marca.id)
                .where(
                    Modelo.deleted_at.is_(None),
                    Marca.deleted_at.is_(None),
                    Marca.id == filters.marca_id,
                )
            )

        stmt = stmt.order_by(Carro.created_at.desc())

        if filters:
            if filters.usuario_id:
                stmt = stmt.where(Carro.usuario_id == filters.usuario_id)
            if filters.modelo_id:
                stmt = stmt.where(Carro.modelo_id == filters.modelo_id)
            if filters.ano is not None:
                stmt = stmt.where(Carro.ano == filters.ano)
            if filters.combustivel:
                stmt = stmt.where(Carro.combustivel == filters.combustivel)

        return self._paginate(stmt, page=page, page_size=page_size)

    def create(self, **fields: object) -> Carro:
        carro = Carro(**fields)
        self.db.add(carro)
        return self._commit_refresh(carro)

    def update(self, carro: Carro, **fields: object) -> Carro:
        for key, value in fields.items():
            setattr(carro, key, value)
        return self._commit_refresh(carro)
