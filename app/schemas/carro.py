import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import TimestampSchema
from app.schemas.validators import (
    AnoValido,
    NumPortasValido,
    QuilometragemValida,
    ValorPositivo,
)
from app.models.combustivel import Combustivel


class CarroCreateRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "modelo_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                    "ano": 2022,
                    "combustivel": "FLEX",
                    "num_portas": 4,
                    "cor": "Prata",
                    "quilometragem": 35000,
                    "valor_anuncio": 98900.00,
                }
            ]
        }
    )

    modelo_id: uuid.UUID
    ano: AnoValido
    combustivel: Combustivel
    num_portas: NumPortasValido
    cor: str = Field(..., min_length=1, max_length=100)
    quilometragem: QuilometragemValida
    valor_anuncio: ValorPositivo


class CarroUpdateRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "ano": 2022,
                    "combustivel": "GASOLINA",
                    "num_portas": 4,
                    "cor": "Preto",
                    "quilometragem": 38000,
                    "valor_anuncio": 95900.00,
                }
            ]
        }
    )

    modelo_id: uuid.UUID | None = None
    ano: AnoValido | None = None
    combustivel: Combustivel | None = None
    num_portas: NumPortasValido | None = None
    cor: str | None = Field(default=None, min_length=1, max_length=100)
    quilometragem: QuilometragemValida | None = None
    valor_anuncio: ValorPositivo | None = None


class CarroResponse(TimestampSchema):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "modelo_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                    "usuario_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "ano": 2022,
                    "combustivel": "FLEX",
                    "num_portas": 4,
                    "cor": "Prata",
                    "quilometragem": 35000,
                    "valor_anuncio": 98900.00,
                    "descricao": "Baixa quilometragem e excelente estado.",
                    "created_at": "2026-01-15T10:30:00Z",
                    "updated_at": "2026-01-15T10:30:00Z",
                    "deleted_at": None,
                }
            ]
        },
    )

    modelo_id: uuid.UUID
    usuario_id: uuid.UUID
    ano: AnoValido
    combustivel: Combustivel
    num_portas: NumPortasValido
    cor: str
    quilometragem: QuilometragemValida
    valor_anuncio: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    descricao: str | None = None
