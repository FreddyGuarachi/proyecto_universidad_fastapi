from typing import Optional, Literal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import carrera
from app.repositories.carrera import CarreraRepository


class CarreraService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CarreraRepository(db)

    def get_or_404(self, carrera_id: int):
        carrera_db = self.repo.find_by_id(carrera_id)

        if carrera_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Carrera not found"
            )
        return carrera_db

    def create(self, carrera_data: carrera.CarreraCreate):
        carrera_db = self.repo.create(carrera_data)

        self.db.commit()
        self.db.refresh(carrera_db)

        return carrera_db

    def find_all(
        self,
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        titulo_otorgado: Optional[str] = None,
        cantidad_materias: Optional[int] = None,
        order_by: Literal["name", "titulo_otorgado", "cantidad_materias"] = "name",
        order_dir: Literal["asc", "desc"] = "asc",
    ):
        return self.repo.find_all(
            skip=skip,
            limit=limit,
            name=name,
            titulo_otorgado=titulo_otorgado,
            cantidad_materias=cantidad_materias,
            order_by=order_by,
            order_dir=order_dir,
        )

    def find_by_id(self, carrera_id: int):
        return self.get_or_404(carrera_id)

    def update(self, carrera_data: carrera.CarreraUpdate, carrera_id: int):
        carrera_db = self.get_or_404(carrera_id)

        self.repo.update(carrera_data=carrera_data, carrera_db=carrera_db)

        self.db.commit()
        self.db.refresh(carrera_db)

        return carrera_db

    def delete(self, carrera_id: int):

        carrera_db = self.get_or_404(carrera_id)

        self.repo.delete(carrera_db)
        self.db.commit()

        return carrera_db
