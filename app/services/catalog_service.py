from sqlalchemy.orm import Session

from app.repositories.catalog_repository import CatalogRepository, CatalogModelRow


class CatalogService:
    def __init__(self, db: Session) -> None:
        self.repository = CatalogRepository(db)

    def list_models(self) -> list[CatalogModelRow]:
        return self.repository.list_models()
