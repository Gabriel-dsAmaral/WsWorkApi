import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.carro import Carro
from app.models.combustivel import Combustivel
from app.repositories.base import PaginatedResult
from app.repositories.car_repository import CarFilters, CarRepository
from app.repositories.model_repository import ModelBrandContext, ModelRepository
from app.schemas.carro import CarroCreateRequest, CarroUpdateRequest
from app.schemas.common import PaginationParams
from app.services.ai_description_service import AIDescriptionService, CarDescriptionContext


class CarService:
    def __init__(self, db: Session) -> None:
        self.repository = CarRepository(db)
        self.model_repository = ModelRepository(db)
        self.ai_description_service = AIDescriptionService()

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
        model_context = self._get_model_context(data.modelo_id)
        car_data = data.model_dump()
        car_data["descricao"] = self._generate_description(car_data, model_context)
        car_data["usuario_id"] = user_id
        return self.repository.create(**car_data)

    def update_for_user(
        self,
        car_id: uuid.UUID,
        user_id: uuid.UUID,
        data: CarroUpdateRequest,
    ) -> Carro:
        carro = self.get_by_id(car_id)
        self._ensure_owner(carro, user_id)

        update_data = data.model_dump(exclude_unset=True)
        merged_data = self._merge_car_data(carro, update_data)
        model_context = self._get_model_context(merged_data["modelo_id"])
        update_data["descricao"] = self._generate_description(merged_data, model_context)

        return self.repository.update(carro, **update_data)

    def delete_for_user(self, car_id: uuid.UUID, user_id: uuid.UUID) -> None:
        carro = self.get_by_id(car_id)
        self._ensure_owner(carro, user_id)
        self.repository.soft_delete(carro)

    def _get_model_context(self, model_id: uuid.UUID) -> ModelBrandContext:
        context = self.model_repository.get_with_brand(model_id)
        if context is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modelo não encontrado",
            )
        return context

    def _generate_description(
        self,
        car_data: dict[str, object],
        model_context: ModelBrandContext,
    ) -> str:
        context = CarDescriptionContext(
            marca=model_context.marca,
            nome_modelo=model_context.nome,
            ano=int(car_data["ano"]),
            combustivel=car_data["combustivel"],
            cor=str(car_data["cor"]),
            quilometragem=int(car_data["quilometragem"]),
            num_portas=int(car_data["num_portas"]),
            valor_anuncio=Decimal(str(car_data["valor_anuncio"])),
            valor_fipe=model_context.valor_fipe,
        )
        return self.ai_description_service.generate(context)

    @staticmethod
    def _merge_car_data(carro: Carro, update_data: dict[str, object]) -> dict[str, object]:
        return {
            "modelo_id": update_data.get("modelo_id", carro.modelo_id),
            "ano": update_data.get("ano", carro.ano),
            "combustivel": update_data.get("combustivel", carro.combustivel),
            "cor": update_data.get("cor", carro.cor),
            "quilometragem": update_data.get("quilometragem", carro.quilometragem),
            "num_portas": update_data.get("num_portas", carro.num_portas),
            "valor_anuncio": update_data.get("valor_anuncio", carro.valor_anuncio),
        }

    @staticmethod
    def _ensure_owner(carro: Carro, user_id: uuid.UUID) -> None:
        if carro.usuario_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para alterar este carro",
            )
