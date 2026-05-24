import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Cars API"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = Field(default_factory=lambda: os.environ["DATABASE_URL"])

    jwt_secret: str = Field(default_factory=lambda: os.getenv("JWT_SECRET", "change-me"))
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = Field(
        default_factory=lambda: int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
