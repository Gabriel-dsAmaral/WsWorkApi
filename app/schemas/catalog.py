import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CatalogModelItem(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                    "nome": "Corolla",
                    "marca": "Toyota",
                    "valor_fipe": 125000.00,
                }
            ]
        },
    )

    id: uuid.UUID
    nome: str
    marca: str
    valor_fipe: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
