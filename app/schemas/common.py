from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field

from app.repositories.base import PaginatedResult

T = TypeVar("T")
R = TypeVar("R", bound=BaseModel)


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list
    total: int
    page: int
    page_size: int
    pages: int


def to_paginated_response(
    result: PaginatedResult[T],
    response_schema: type[R],
) -> PaginatedResponse:
    return PaginatedResponse(
        items=[response_schema.model_validate(item) for item in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        pages=result.pages,
    )
