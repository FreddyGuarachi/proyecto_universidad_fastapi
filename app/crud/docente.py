from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Literal
from app.models.docente import Docente
from app.schemas.docente import DocenteCreate, DocenteUpdate


def create_docente(docente_data: DocenteCreate, db: Session):

    db_docente = Docente(**docente_data.model_dump())

    db.add(db_docente)
    db.commit()
    db.refresh(db_docente)
    return db_docente


def get_docentes(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    matricula: Optional[str] = None,
    dni: Optional[str] = None,
    email: Optional[str] = None,
    order_by: Literal["name", "matricula", "dni", "email"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
):
    query = db.query(Docente)

    if name:
        query = query.filter(Docente.name.ilike(f"%{name}%"))
    if matricula:
        query = query.filter(Docente.matricula.ilike(f"%{matricula}%"))
    if dni:
        query = query.filter(Docente.dni.ilike(f"%{dni}%"))
    if email:
        query = query.filter(Docente.email.ilike(f"%{email}%"))

    total = query.count()

    column = getattr(Docente, order_by)

    column = column.desc() if order_dir == "desc" else column.asc()

    items = query.order_by(column).offset(skip).limit(limit).all()

    return {"items": items, "total": total}


def get_docente_by_id(docente_id: int, db: Session):

    docente_db = db.query(Docente).filter(Docente.id == docente_id).first()

    if docente_db is None:
        raise HTTPException(status_code=404, detail="Docente not found")

    return docente_db


def update_docente(docente_data: DocenteUpdate, docente_id: int, db: Session):

    docente_db = db.query(Docente).filter(Docente.id == docente_id).first()

    if docente_db is None:
        raise HTTPException(status_code=404, detail="Docente not found")

    for key, value in docente_data.model_dump(exclude_unset=True).items():
        setattr(docente_db, key, value)

    db.commit()
    db.refresh(docente_db)
    return docente_db


def delete_docente(docente_id: int, db: Session):

    docente_db = db.query(Docente).filter(Docente.id == docente_id).first()

    if docente_db is None:
        raise HTTPException(status_code=404, detail="Docente not found")

    db.delete(docente_db)
    db.commit()
    return docente_db
