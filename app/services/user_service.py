import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.repositories.base import PaginatedResult
from app.repositories.user_repository import UserFilters, UserRepository
from app.schemas.common import PaginationParams
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


class UserService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def get_by_id(self, user_id: uuid.UUID) -> Usuario:
        usuario = self.repository.get_by_id(user_id)
        if usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return usuario

    def list(
        self,
        *,
        filters: UserFilters | None = None,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult[Usuario]:
        params = pagination or PaginationParams()
        return self.repository.list(
            filters=filters,
            page=params.page,
            page_size=params.page_size,
        )

    def create(self, data: UsuarioCreate) -> Usuario:
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

    def update(self, user_id: uuid.UUID, data: UsuarioUpdate) -> Usuario:
        usuario = self.get_by_id(user_id)
        update_data = data.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing = self.repository.get_by_email(update_data["email"])
            if existing and existing.id != usuario.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="E-mail já cadastrado",
                )

        if "senha" in update_data:
            update_data["senha_hash"] = hash_password(update_data.pop("senha"))

        return self.repository.update(usuario, **update_data)

    def delete(self, user_id: uuid.UUID) -> None:
        usuario = self.get_by_id(user_id)
        self.repository.soft_delete(usuario)
