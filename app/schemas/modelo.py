import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import TimestampSchema
from app.schemas.validators import IconeUrl, NomeCurto, ValorPositivo


class ModeloCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "marca_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "nome": "Corolla",
                    "valor_fipe": 125000.00,
                    "icone": "https://cdn.example.com/modelos/corolla.svg",
                }
            ]
        }
    )

    marca_id: uuid.UUID
    nome: NomeCurto
    valor_fipe: ValorPositivo
    icone: IconeUrl = None


class ModeloUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "marca_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "nome": "Corolla XEi",
                    "valor_fipe": 128500.50,
                    "icone": "https://cdn.example.com/modelos/corolla-xei.svg",
                }
            ]
        }
    )

    marca_id: uuid.UUID | None = None
    nome: NomeCurto | None = None
    valor_fipe: ValorPositivo | None = None
    icone: IconeUrl | None = None


class ModeloResponse(TimestampSchema):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                    "marca_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "nome": "Corolla",
                    "valor_fipe": 125000.00,
                    "icone": "https://cdn.example.com/modelos/corolla.svg",
                    "created_at": "2026-01-15T10:30:00Z",
                    "updated_at": "2026-01-15T10:30:00Z",
                    "deleted_at": None,
                }
            ]
        },
    )

    marca_id: uuid.UUID
    nome: str
    valor_fipe: ValorPositivo
    icone: str | None = None
