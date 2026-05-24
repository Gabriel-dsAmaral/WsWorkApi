from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.base import TimestampSchema
from app.schemas.carro import CarroCreateRequest, CarroResponse, CarroUpdateRequest
from app.schemas.catalog import CatalogModelItem
from app.schemas.common import PaginatedResponse, PaginationParams, to_paginated_response
from app.schemas.marca import MarcaCreate, MarcaResponse, MarcaUpdate
from app.schemas.modelo import ModeloCreate, ModeloResponse, ModeloUpdate
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate

__all__ = [
    "TimestampSchema",
    "LoginRequest",
    "TokenResponse",
    "PaginatedResponse",
    "PaginationParams",
    "to_paginated_response",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "MarcaCreate",
    "MarcaUpdate",
    "MarcaResponse",
    "ModeloCreate",
    "ModeloUpdate",
    "ModeloResponse",
    "CarroCreateRequest",
    "CarroUpdateRequest",
    "CarroResponse",
    "CatalogModelItem",
]
