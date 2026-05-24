from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.include_router(router)

    @app.get("/", tags=["root"])
    def home() -> dict[str, str]:
        return {"message": f"{settings.app_name} running"}

    return app


app = create_app()
