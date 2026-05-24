import enum


class Combustivel(str, enum.Enum):
    FLEX = "FLEX"
    GASOLINA = "GASOLINA"
    DIESEL = "DIESEL"
    ELETRICO = "ELETRICO"
    HIBRIDO = "HIBRIDO"
