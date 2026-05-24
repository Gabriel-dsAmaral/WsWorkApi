import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.modelo import Modelo
from app.repositories.base import PaginatedResult
from app.repositories.brand_repository import BrandRepository
from app.repositories.model_repository import ModelFilters, ModelRepository
from app.schemas.common import PaginationParams
from app.schemas.modelo import ModeloCreate, ModeloUpdate


class ModelService:
    def __init__(self, db: Session) -> None:
        self.repository = ModelRepository(db)
        self.brand_repository = BrandRepository(db)

    def get_by_id(self, model_id: uuid.UUID) -> Modelo:
        modelo = self.repository.get_by_id(model_id)
        if modelo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modelo não encontrado")
        return modelo

    def list(
        self,
        *,
        filters: ModelFilters | None = None,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult[Modelo]:
        params = pagination or PaginationParams()
        return self.repository.list(
            filters=filters,
            page=params.page,
            page_size=params.page_size,
        )

    def create(self, data: ModeloCreate) -> Modelo:
        self._ensure_brand_exists(data.marca_id)
        return self.repository.create(
            marca_id=data.marca_id,
            nome=data.nome,
            valor_fipe=data.valor_fipe,
            icone=data.icone,
        )

    def update(self, model_id: uuid.UUID, data: ModeloUpdate) -> Modelo:
        modelo = self.get_by_id(model_id)
        update_data = data.model_dump(exclude_unset=True)

        if "marca_id" in update_data:
            self._ensure_brand_exists(update_data["marca_id"])

        return self.repository.update(modelo, **update_data)

    def delete(self, model_id: uuid.UUID) -> None:
        modelo = self.get_by_id(model_id)
        self.repository.soft_delete(modelo)

    def _ensure_brand_exists(self, brand_id: uuid.UUID) -> None:
        if self.brand_repository.get_by_id(brand_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marca não encontrada",
            )
