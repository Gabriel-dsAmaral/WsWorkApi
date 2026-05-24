import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.marca import Marca
from app.repositories.base import PaginatedResult
from app.repositories.brand_repository import BrandFilters, BrandRepository
from app.schemas.common import PaginationParams
from app.schemas.marca import MarcaCreate, MarcaUpdate


class BrandService:
    def __init__(self, db: Session) -> None:
        self.repository = BrandRepository(db)

    def get_by_id(self, brand_id: uuid.UUID) -> Marca:
        marca = self.repository.get_by_id(brand_id)
        if marca is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marca não encontrada")
        return marca

    def list(
        self,
        *,
        filters: BrandFilters | None = None,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult[Marca]:
        params = pagination or PaginationParams()
        return self.repository.list(
            filters=filters,
            page=params.page,
            page_size=params.page_size,
        )

    def create(self, data: MarcaCreate) -> Marca:
        existing = self.repository.get_by_name(data.nome_marca)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Marca já cadastrada",
            )
        return self.repository.create(nome_marca=data.nome_marca, icone=data.icone)

    def update(self, brand_id: uuid.UUID, data: MarcaUpdate) -> Marca:
        marca = self.get_by_id(brand_id)
        update_data = data.model_dump(exclude_unset=True)

        if "nome_marca" in update_data:
            existing = self.repository.get_by_name(update_data["nome_marca"])
            if existing and existing.id != marca.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Marca já cadastrada",
                )

        return self.repository.update(marca, **update_data)

    def delete(self, brand_id: uuid.UUID) -> None:
        marca = self.get_by_id(brand_id)
        self.repository.soft_delete(marca)
