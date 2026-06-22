from typing import Optional, Literal

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.carrera import Carrera
from app.schemas import carrera


class CarreraRepository:

    ORDER_FIELDS = {
        "name": Carrera.name,
        "titulo_otorgado": Carrera.titulo_otorgado,
        "cantidad_materias": Carrera.cantidad_materias,
    }

    def __init__(self, db: Session):
        self.db = db

    def create(self, carrera_data: carrera.CarreraCreate):
        carrera_db = Carrera(**carrera_data.model_dump())

        self.db.add(carrera_db)

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
        stmt = select(Carrera)

        # filtros

        if name:
            stmt = stmt.where(Carrera.name.ilike(f"%{name}%"))
        if titulo_otorgado:
            stmt = stmt.where(Carrera.titulo_otorgado.ilike(f"%{titulo_otorgado}%"))
        if cantidad_materias is not None:
            stmt = stmt.where(Carrera.cantidad_materias == cantidad_materias)

        # total

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.scalar(count_stmt) or 0

        # orden

        column = self.ORDER_FIELDS[order_by]
        column = column.desc() if order_dir == "desc" else column.asc()
        stmt = stmt.order_by(column)

        # paginacion

        stmt = stmt.offset(skip).limit(limit)

        items = self.db.scalars(stmt).all()

        return {"total": total, "items": items}

    def find_by_id(self, carrera_id: int):
        stmt = select(Carrera).where(Carrera.id == carrera_id)

        return self.db.scalar(stmt)

    def update(self, carrera_data: carrera.CarreraUpdate, carrera_db: Carrera):

        for key, value in carrera_data.model_dump(exclude_unset=True).items():
            setattr(carrera_db, key, value)

        return carrera_db

    def delete(self, carrera_db: Carrera):
        self.db.delete(carrera_db)

        return carrera_db
