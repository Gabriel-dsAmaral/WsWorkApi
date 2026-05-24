import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.modelo import Modelo
from app.models.usuario import Usuario
from app.repositories.model_repository import ModelFilters
from app.routes.deps import get_pagination
from app.schemas.common import PaginatedResponse, PaginationParams, to_paginated_response
from app.schemas.modelo import ModeloCreate, ModeloResponse, ModeloUpdate
from app.services.model_service import ModelService

router = APIRouter(prefix="/modelos", tags=["modelos"])


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Listar modelos",
)
def list_models(
    nome: str | None = Query(None, description="Filtrar por nome do modelo"),
    marca_id: uuid.UUID | None = Query(None, description="Filtrar por marca"),
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> PaginatedResponse:
    result = ModelService(db).list(
        filters=ModelFilters(nome=nome, marca_id=marca_id),
        pagination=pagination,
    )
    return to_paginated_response(result, ModeloResponse)


@router.get(
    "/{model_id}",
    response_model=ModeloResponse,
    summary="Obter modelo por ID",
)
def get_model(
    model_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Modelo:
    return ModelService(db).get_by_id(model_id)


@router.post(
    "",
    response_model=ModeloResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar modelo",
)
def create_model(
    payload: ModeloCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Modelo:
    return ModelService(db).create(payload)


@router.patch(
    "/{model_id}",
    response_model=ModeloResponse,
    summary="Atualizar modelo",
)
def update_model(
    model_id: uuid.UUID,
    payload: ModeloUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Modelo:
    return ModelService(db).update(model_id, payload)


@router.delete(
    "/{model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir modelo",
)
def delete_model(
    model_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> None:
    ModelService(db).delete(model_id)
