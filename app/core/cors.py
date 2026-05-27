from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]

CORS_ALLOW_HEADERS = [
    "Authorization",
    "Content-Type",
    "Accept",
    "Origin",
    "X-Requested-With",
]

CORS_EXPOSE_HEADERS = ["Content-Length", "Content-Type"]

CORS_MAX_AGE_SECONDS = 600


def setup_cors(app: FastAPI, settings: Settings) -> None:
    middleware_kwargs: dict = {
        "allow_origins": settings.cors_origins,
        "allow_credentials": settings.cors_allow_credentials,
        "allow_methods": CORS_ALLOW_METHODS,
        "allow_headers": CORS_ALLOW_HEADERS,
        "expose_headers": CORS_EXPOSE_HEADERS,
        "max_age": CORS_MAX_AGE_SECONDS,
    }

    if settings.cors_origin_regex:
        middleware_kwargs["allow_origin_regex"] = settings.cors_origin_regex

    app.add_middleware(CORSMiddleware, **middleware_kwargs)
