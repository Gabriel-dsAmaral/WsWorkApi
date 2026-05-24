from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import TimestampSchema
from app.schemas.validators import IconeUrl, NomeCurto


class MarcaCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nome_marca": "Toyota",
                    "icone": "https://cdn.example.com/marcas/toyota.svg",
                }
            ]
        }
    )

    nome_marca: NomeCurto
    icone: IconeUrl = None


class MarcaUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nome_marca": "Toyota Motor",
                    "icone": "https://cdn.example.com/marcas/toyota-novo.svg",
                }
            ]
        }
    )

    nome_marca: NomeCurto | None = None
    icone: IconeUrl | None = None


class MarcaResponse(TimestampSchema):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "nome_marca": "Toyota",
                    "icone": "https://cdn.example.com/marcas/toyota.svg",
                    "created_at": "2026-01-15T10:30:00Z",
                    "updated_at": "2026-01-15T10:30:00Z",
                    "deleted_at": None,
                }
            ]
        },
    )

    nome_marca: str = Field(..., description="Nome da marca")
    icone: str | None = None
