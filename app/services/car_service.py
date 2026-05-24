import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.carro import Carro
from app.repositories.base import PaginatedResult
from app.repositories.car_repository import CarFilters, CarRepository
from app.repositories.model_repository import ModelRepository
from app.schemas.carro import CarroCreateRequest, CarroUpdateRequest
from app.schemas.common import PaginationParams


class CarService:
    def __init__(self, db: Session) -> None:
        self.repository = CarRepository(db)
        self.model_repository = ModelRepository(db)

    def get_by_id(self, car_id: uuid.UUID) -> Carro:
        carro = self.repository.get_by_id(car_id)
        if carro is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado")
        return carro

    def list(
        self,
        *,
        filters: CarFilters | None = None,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult[Carro]:
        params = pagination or PaginationParams()
        return self.repository.list(
            filters=filters,
            page=params.page,
            page_size=params.page_size,
        )

    def create_for_user(self, user_id: uuid.UUID, data: CarroCreateRequest) -> Carro:
        self._ensure_model_exists(data.modelo_id)
        return self.repository.create(**data.model_dump(), usuario_id=user_id)

    def update_for_user(
        self,
        car_id: uuid.UUID,
        user_id: uuid.UUID,
        data: CarroUpdateRequest,
    ) -> Carro:
        carro = self.get_by_id(car_id)
        self._ensure_owner(carro, user_id)

        update_data = data.model_dump(exclude_unset=True)
        if "modelo_id" in update_data:
            self._ensure_model_exists(update_data["modelo_id"])

        return self.repository.update(carro, **update_data)

    def delete_for_user(self, car_id: uuid.UUID, user_id: uuid.UUID) -> None:
        carro = self.get_by_id(car_id)
        self._ensure_owner(carro, user_id)
        self.repository.soft_delete(carro)

    def _ensure_model_exists(self, model_id: uuid.UUID) -> None:
        if self.model_repository.get_by_id(model_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modelo não encontrado",
            )

    @staticmethod
    def _ensure_owner(carro: Carro, user_id: uuid.UUID) -> None:
        if carro.usuario_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para alterar este carro",
            )
