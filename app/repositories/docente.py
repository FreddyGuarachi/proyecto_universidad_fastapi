from typing import Optional, Literal


from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.docente import Docente
from app.schemas import docente


class DocenteRepository:

    ORDER_FIELDS = {
        "name": Docente.name,
        "matricula": Docente.matricula,
        "dni": Docente.dni,
        "email": Docente.email,
    }

    def __init__(self, db: Session):
        self.db = db

    def create(self, docente_data: docente.DocenteCreate):

        docente_db = Docente(**docente_data.model_dump())

        self.db.add(docente_db)

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
        stmt = select(Docente)

        # filtros

        if name:
            stmt = stmt.where(Docente.name.ilike(f"%{name}%"))
        if matricula:
            stmt = stmt.where(Docente.matricula.ilike(f"%{matricula}%"))
        if dni:
            stmt = stmt.where(Docente.dni.ilike(f"%{dni}%"))
        if email:
            stmt = stmt.where(Docente.email.ilike(f"%{email}%"))

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

    def find_by_id(self, docente_id: int):
        stmt = select(Docente).where(Docente.id == docente_id)

        return self.db.scalar(stmt)

    def update(self, docente_data: docente.DocenteUpdate, docente_db: Docente):

        for key, value in docente_data.model_dump(exclude_unset=True).items():
            setattr(docente_db, key, value)

        return docente_db

    def delete(self, docente_db: Docente):
        self.db.delete(docente_db)

        return docente_db
