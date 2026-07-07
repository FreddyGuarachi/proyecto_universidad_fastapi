from typing import Literal, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.alumno import Alumno
from app.schemas import alumno


class AlumnoRepository:

    ORDER_FIELDS = {
        "name": Alumno.name,
        "dni": Alumno.dni,
        "email": Alumno.email,
    }

    def __init__(self, db: Session):
        self.db = db

    def create(self, alumno_data: alumno.AlumnoCreate):
        alumno_db = Alumno(**alumno_data.model_dump())

        self.db.add(alumno_db)

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
        stmt = select(Alumno)

        # filtros

        if name:
            stmt = stmt.where(Alumno.name.ilike(f"%{name}%"))
        if dni:
            stmt = stmt.where(Alumno.dni.ilike(f"%{dni}%"))
        if email:
            stmt = stmt.where(Alumno.email.ilike(f"%{email}%"))

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

        return {"items": items, "total": total}

    def find_by_id(self, alumno_id: int):
        stmt = select(Alumno).where(Alumno.id == alumno_id)

        return self.db.scalar(stmt)

    def update(self, alumno_data: alumno.AlumnoUpdate, alumno_db: Alumno):

        for key, value in alumno_data.model_dump(exclude_unset=True).items():
            setattr(alumno_db, key, value)

        return alumno_db

    def delete(self, alumno_db: Alumno):
        self.db.delete(alumno_db)

        return alumno_db
