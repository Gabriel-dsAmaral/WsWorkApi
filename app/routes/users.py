import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.usuario import Usuario
from app.repositories.user_repository import UserFilters
from app.routes.deps import get_pagination
from app.schemas.common import PaginatedResponse, PaginationParams, to_paginated_response
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Listar usuários",
)
def list_users(
    nome: str | None = Query(None, description="Filtrar por nome"),
    email: str | None = Query(None, description="Filtrar por e-mail"),
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> PaginatedResponse:
    result = UserService(db).list(
        filters=UserFilters(nome=nome, email=email),
        pagination=pagination,
    )
    return to_paginated_response(result, UsuarioResponse)


@router.get(
    "/{user_id}",
    response_model=UsuarioResponse,
    summary="Obter usuário por ID",
)
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Usuario:
    return UserService(db).get_by_id(user_id)


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário",
)
def create_user(
    payload: UsuarioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Usuario:
    return UserService(db).create(payload)


@router.patch(
    "/{user_id}",
    response_model=UsuarioResponse,
    summary="Atualizar usuário",
)
def update_user(
    user_id: uuid.UUID,
    payload: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Usuario:
    return UserService(db).update(user_id, payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir usuário",
)
def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> None:
    UserService(db).delete(user_id)
