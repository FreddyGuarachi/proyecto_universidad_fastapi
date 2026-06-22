from typing import Literal, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import alumno
from app.repositories.alumno_repository import AlumnoRepository


class AlumnoService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = AlumnoRepository(db)

    def get_or_404(self, alumno_id: int):
        alumno_db = self.repo.find_by_id(alumno_id)

        if alumno_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Alumno not found"
            )
        return alumno_db

    def create(self, alumno_data: alumno.AlumnoCreate):
        alumno_db = self.repo.create(alumno_data)

        self.db.commit()
        self.db.refresh(alumno_db)

        return alumno_db

    def find_all(
        self,
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        dni: Optional[str] = None,
        email: Optional[str] = None,
        order_by: Literal["name", "dni", "email"] = "name",
        order_dir: Literal["asc", "desc"] = "asc",
    ):
        return self.repo.find_all(
            skip=skip,
            limit=limit,
            name=name,
            dni=dni,
            email=email,
            order_by=order_by,
            order_dir=order_dir,
        )

    def find_by_id(self, alumno_id: int):
        return self.get_or_404(alumno_id)

    def update(self, alumno_data: alumno.AlumnoUpdate, alumno_id: int):
        alumno_db = self.get_or_404(alumno_id)

        self.repo.update(alumno_data=alumno_data, alumno_db=alumno_db)

        self.db.commit()
        self.db.refresh(alumno_db)

        return alumno_db

    def delete(self, alumno_id: int):
        alumno_db = self.get_or_404(alumno_id)

        self.repo.delete(alumno_db)
        self.db.commit()

        return alumno_db
