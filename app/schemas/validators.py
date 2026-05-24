from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import Field

ANO_ATUAL = datetime.now().year

AnoValido = Annotated[int, Field(ge=1900, le=ANO_ATUAL + 1)]
ValorPositivo = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
QuilometragemValida = Annotated[int, Field(ge=0)]
NumPortasValido = Annotated[int, Field(ge=2, le=5)]
SenhaMinima = Annotated[str, Field(min_length=8, max_length=128)]
NomeCurto = Annotated[str, Field(min_length=1, max_length=255)]
DescricaoCurta = Annotated[str | None, Field(max_length=2000)]
IconeUrl = Annotated[str | None, Field(max_length=512)]
