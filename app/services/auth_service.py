from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.usuario import Usuario
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.usuario import UsuarioCreate


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def register(self, data: UsuarioCreate) -> Usuario:
        if self.repository.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado",
            )

        return self.repository.create(
            nome=data.nome,
            email=data.email,
            senha_hash=hash_password(data.senha),
            descricao=data.descricao,
        )

    def login(self, data: LoginRequest) -> TokenResponse:
        usuario = self.repository.get_by_email(data.email)

        if usuario is None or not verify_password(data.senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenResponse(access_token=create_access_token(usuario.id))
