import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from app.core.cors_origins import (
    get_cors_allow_credentials_from_env,
    get_cors_origin_regex_from_env,
    get_cors_origins_from_env,
)

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

    cors_origins: list[str] = Field(default_factory=get_cors_origins_from_env)
    cors_origin_regex: str | None = Field(default_factory=get_cors_origin_regex_from_env)
    cors_allow_credentials: bool = Field(default_factory=get_cors_allow_credentials_from_env)

    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
