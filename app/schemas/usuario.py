from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.base import TimestampSchema
from app.schemas.validators import DescricaoCurta, NomeCurto, SenhaMinima


class UsuarioCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nome": "Gabriel Amaral",
                    "email": "gabriel@example.com",
                    "senha": "senha1234",
                    "descricao": "Vendedor de veículos seminovos.",
                }
            ]
        }
    )

    nome: NomeCurto
    email: EmailStr
    senha: SenhaMinima
    descricao: DescricaoCurta = None


class UsuarioUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nome": "Gabriel Amaral",
                    "email": "gabriel.novo@example.com",
                    "senha": "novaSenha123",
                    "descricao": "Perfil atualizado.",
                }
            ]
        }
    )

    nome: NomeCurto | None = None
    email: EmailStr | None = None
    senha: SenhaMinima | None = None
    descricao: DescricaoCurta | None = None


class UsuarioResponse(TimestampSchema):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "nome": "Gabriel Amaral",
                    "email": "gabriel@example.com",
                    "descricao": "Vendedor de veículos seminovos.",
                    "created_at": "2026-01-15T10:30:00Z",
                    "updated_at": "2026-01-15T10:30:00Z",
                    "deleted_at": None,
                }
            ]
        },
    )

    nome: str
    email: EmailStr
    descricao: str | None = None
