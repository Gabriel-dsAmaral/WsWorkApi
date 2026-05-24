from fastapi import Query

from app.schemas.common import PaginationParams


def get_pagination(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)
