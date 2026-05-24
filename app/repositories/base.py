from dataclasses import dataclass
from typing import Any, Generic, TypeVar
import uuid
from datetime import UTC, datetime

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.base import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


@dataclass
class PaginatedResult(Generic[ModelT]):
    items: list[ModelT]
    total: int
    page: int
    page_size: int

    @property
    def pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size if self.page_size else 0


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, db: Session) -> None:
        self.db = db

    def _active(self, stmt: Select[Any]) -> Select[Any]:
        return stmt.where(self.model.deleted_at.is_(None))

    def get_by_id(self, entity_id: uuid.UUID) -> ModelT | None:
        stmt = self._active(select(self.model)).where(self.model.id == entity_id)
        return self.db.scalars(stmt).first()

    def soft_delete(self, entity: ModelT) -> ModelT:
        entity.deleted_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def _paginate(
        self,
        stmt: Select[Any],
        *,
        page: int,
        page_size: int,
    ) -> PaginatedResult[ModelT]:
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.scalar(count_stmt) or 0
        items = list(
            self.db.scalars(
                stmt.offset((page - 1) * page_size).limit(page_size)
            ).all()
        )
        return PaginatedResult(items=items, total=total, page=page, page_size=page_size)

    def _commit_refresh(self, entity: ModelT) -> ModelT:
        self.db.commit()
        self.db.refresh(entity)
        return entity
