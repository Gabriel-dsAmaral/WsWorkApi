from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.catalog import CatalogModelItem
from app.services.catalog_service import CatalogService

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get(
    "/models",
    response_model=list[CatalogModelItem],
    summary="Listar catálogo de modelos",
)
def list_catalog_models(db: Session = Depends(get_db)) -> list[CatalogModelItem]:
    rows = CatalogService(db).list_models()
    return [
        CatalogModelItem(
            id=row.id,
            nome=row.nome,
            marca=row.marca,
            valor_fipe=row.valor_fipe,
        )
        for row in rows
    ]
