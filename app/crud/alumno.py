from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Literal
from app.models.alumno import Alumno
from app.schemas.alumno import AlumnoCreate, AlumnoUpdate


def create_alumno(alumno_data: AlumnoCreate, db: Session):

    db_alumno = Alumno(**alumno_data.model_dump())

    db.add(db_alumno)
    db.commit()
    db.refresh(db_alumno)
    return db_alumno


def upload_image_alumno(db: Session, alumno_id: int, image_path: str):

    alumno = get_alumno_by_id(alumno_id=alumno_id, db=db)

    alumno.foto_perfil = image_path

    db.commit()
    db.refresh(alumno)

    return alumno


def get_alumnos(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    dni: Optional[str] = None,
    email: Optional[str] = None,
    order_by: Literal["name", "dni", "email"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
):
    query = db.query(Alumno)

    if name:
        query = query.filter(Alumno.name.ilike(f"%{name}%"))
    if dni:
        query = query.filter(Alumno.dni.ilike(f"%{dni}%"))
    if email:
        query = query.filter(Alumno.email.ilike(f"%{email}%"))

    total = query.count()

    column = getattr(Alumno, order_by)

    column = column.desc() if order_dir == "desc" else column.asc()

    items = query.order_by(column).offset(skip).limit(limit).all()

    return {"items": items, "total": total}


def get_alumno_by_id(alumno_id: int, db: Session):

    alumno_db = db.query(Alumno).filter(Alumno.id == alumno_id).first()

    if alumno_db is None:
        raise HTTPException(status_code=404, detail="Alumno not found")

    return alumno_db


def update_alumno(alumno_data: AlumnoUpdate, alumno_id: int, db: Session):

    alumno_db = db.query(Alumno).filter(Alumno.id == alumno_id).first()

    if alumno_db is None:
        raise HTTPException(status_code=404, detail="Alumno not found")

    for key, value in alumno_data.model_dump(exclude_unset=True).items():
        setattr(alumno_db, key, value)

    db.commit()
    db.refresh(alumno_db)
    return alumno_db


def delete_alumno(alumno_id: int, db: Session):

    alumno_db = db.query(Alumno).filter(Alumno.id == alumno_id).first()

    if alumno_db is None:
        raise HTTPException(status_code=404, detail="Alumno not found")

    db.delete(alumno_db)
    db.commit()
    return alumno_db
