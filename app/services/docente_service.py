from typing import Optional, Literal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import docente
from app.repositories.docente_repository import DocenteRepository


class DocenteService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = DocenteRepository(db)

    def get_or_404(self, docente_id: int):
        docente_db = self.repo.find_by_id(docente_id)

        if docente_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Docente not found"
            )

        return docente_db

    def create(self, docente_data: docente.DocenteCreate):
        docente_db = self.repo.create(docente_data)

        self.db.commit()
        self.db.refresh(docente_db)

        return docente_db

    def find_all(
        self,
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        matricula: Optional[str] = None,
        dni: Optional[str] = None,
        email: Optional[str] = None,
        order_by: Literal["name", "matricula", "dni", "email"] = "name",
        order_dir: Literal["asc", "desc"] = "asc",
    ):
        return self.repo.find_all(
            skip=skip,
            limit=limit,
            name=name,
            matricula=matricula,
            dni=dni,
            email=email,
            order_by=order_by,
            order_dir=order_dir,
        )

    def find_by_id(self, docente_id: int):
        return self.get_or_404(docente_id)

    def update(self, docente_data: docente.DocenteUpdate, docente_id: int):
        docente_db = self.get_or_404(docente_id)

        self.repo.update(docente_data=docente_data, docente_db=docente_db)

        self.db.commit()
        self.db.refresh(docente_db)

        return docente_db

    def delete(self, docente_id: int):
        docente_db = self.get_or_404(docente_id)

        self.repo.delete(docente_db)
        self.db.commit()

        return docente_db
