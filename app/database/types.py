import uuid

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

UUID_TYPE = PG_UUID(as_uuid=True)


def uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(
        UUID_TYPE,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )


def uuid_fk(column: str, *, index: bool = False) -> Mapped[uuid.UUID]:
    return mapped_column(
        UUID_TYPE,
        ForeignKey(column),
        nullable=False,
        index=index,
    )
