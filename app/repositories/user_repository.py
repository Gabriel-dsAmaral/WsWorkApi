from dataclasses import dataclass
import uuid

from sqlalchemy import select

from app.models.usuario import Usuario
from app.repositories.base import BaseRepository, PaginatedResult


@dataclass
class UserFilters:
    nome: str | None = None
    email: str | None = None


class UserRepository(BaseRepository[Usuario]):
    model = Usuario

    def get_by_email(self, email: str) -> Usuario | None:
        stmt = self._active(select(Usuario)).where(Usuario.email == email)
        return self.db.scalars(stmt).first()

    def list(
        self,
        *,
        filters: UserFilters | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedResult[Usuario]:
        stmt = self._active(select(Usuario).order_by(Usuario.created_at.desc()))

        if filters:
            if filters.nome:
                stmt = stmt.where(Usuario.nome.ilike(f"%{filters.nome}%"))
            if filters.email:
                stmt = stmt.where(Usuario.email.ilike(f"%{filters.email}%"))

        return self._paginate(stmt, page=page, page_size=page_size)

    def create(
        self,
        *,
        nome: str,
        email: str,
        senha_hash: str,
        descricao: str | None = None,
    ) -> Usuario:
        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            descricao=descricao,
        )
        self.db.add(usuario)
        return self._commit_refresh(usuario)

    def update(self, usuario: Usuario, **fields: object) -> Usuario:
        for key, value in fields.items():
            setattr(usuario, key, value)
        return self._commit_refresh(usuario)
