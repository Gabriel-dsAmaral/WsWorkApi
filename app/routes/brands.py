import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.marca import Marca
from app.models.usuario import Usuario
from app.repositories.brand_repository import BrandFilters
from app.routes.deps import get_pagination
from app.schemas.common import PaginatedResponse, PaginationParams, to_paginated_response
from app.schemas.marca import MarcaCreate, MarcaResponse, MarcaUpdate
from app.services.brand_service import BrandService

router = APIRouter(prefix="/marcas", tags=["marcas"])


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Listar marcas",
)
def list_brands(
    nome_marca: str | None = Query(None, description="Filtrar por nome da marca"),
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> PaginatedResponse:
    result = BrandService(db).list(
        filters=BrandFilters(nome_marca=nome_marca),
        pagination=pagination,
    )
    return to_paginated_response(result, MarcaResponse)


@router.get(
    "/{brand_id}",
    response_model=MarcaResponse,
    summary="Obter marca por ID",
)
def get_brand(
    brand_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Marca:
    return BrandService(db).get_by_id(brand_id)


@router.post(
    "",
    response_model=MarcaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar marca",
)
def create_brand(
    payload: MarcaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Marca:
    return BrandService(db).create(payload)


@router.patch(
    "/{brand_id}",
    response_model=MarcaResponse,
    summary="Atualizar marca",
)
def update_brand(
    brand_id: uuid.UUID,
    payload: MarcaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Marca:
    return BrandService(db).update(brand_id, payload)


@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir marca",
)
def delete_brand(
    brand_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> None:
    BrandService(db).delete(brand_id)
