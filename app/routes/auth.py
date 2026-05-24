from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuário",
)
def register(
    payload: UsuarioCreate,
    db: Session = Depends(get_db),
) -> Usuario:
    return AuthService(db).register(payload)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticar usuário",
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return AuthService(db).login(payload)


@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Obter usuário autenticado",
)
def me(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    return current_user
