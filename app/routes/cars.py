import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.carro import Carro
from app.models.combustivel import Combustivel
from app.models.usuario import Usuario
from app.repositories.car_repository import CarFilters
from app.routes.deps import get_pagination
from app.schemas.carro import CarroCreateRequest, CarroResponse, CarroUpdateRequest
from app.schemas.common import PaginatedResponse, PaginationParams, to_paginated_response
from app.services.car_service import CarService

router = APIRouter(prefix="/carros", tags=["carros"])


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Listar carros",
)
def list_cars(
    marca: uuid.UUID | None = Query(None, description="Filtrar por ID da marca"),
    modelo: uuid.UUID | None = Query(None, description="Filtrar por ID do modelo"),
    ano: int | None = Query(None, ge=1900, description="Filtrar por ano"),
    combustivel: Combustivel | None = Query(None, description="Filtrar por combustível"),
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> PaginatedResponse:
    result = CarService(db).list(
        filters=CarFilters(
            marca_id=marca,
            modelo_id=modelo,
            ano=ano,
            combustivel=combustivel,
        ),
        pagination=pagination,
    )
    return to_paginated_response(result, CarroResponse)


@router.get(
    "/{car_id}",
    response_model=CarroResponse,
    summary="Obter carro por ID",
)
def get_car(
    car_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Carro:
    return CarService(db).get_by_id(car_id)


@router.post(
    "",
    response_model=CarroResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar carro",
)
def create_car(
    payload: CarroCreateRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> Carro:
    return CarService(db).create_for_user(current_user.id, payload)


@router.patch(
    "/{car_id}",
    response_model=CarroResponse,
    summary="Atualizar carro",
)
def update_car(
    car_id: uuid.UUID,
    payload: CarroUpdateRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> Carro:
    return CarService(db).update_for_user(car_id, current_user.id, payload)


@router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir carro",
)
def delete_car(
    car_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> None:
    CarService(db).delete_for_user(car_id, current_user.id)
