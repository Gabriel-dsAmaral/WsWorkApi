from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.brands import router as brands_router
from app.routes.cars import router as cars_router
from app.routes.catalog import router as catalog_router
from app.routes.models import router as models_router
from app.routes.users import router as users_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(brands_router)
router.include_router(models_router)
router.include_router(cars_router)
router.include_router(catalog_router)


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
