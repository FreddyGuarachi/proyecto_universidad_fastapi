from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Literal
from app.models.carrera import Carrera
from app.schemas.carrera import CarreraCreate, CarreraUpdate


def create_carrera(carrera_data: CarreraCreate, db: Session):

    db_carrera = Carrera(**carrera_data.model_dump())

    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)

    return db_carrera


def get_carreras(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    titulo_otorgado: Optional[str] = None,
    cantidad_materias: Optional[int] = None,
    order_by: Literal["name", "titulo_otorgado", "cantidad_materias"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
):
    query = db.query(Carrera)

    if name:
        query = query.filter(Carrera.name.ilike(f"%{name}%"))

    if titulo_otorgado:
        query = query.filter(Carrera.titulo_otorgado.ilike(f"%{titulo_otorgado}%"))

    if cantidad_materias:
        query = query.filter(Carrera.cantidad_materias.ilike(f"%{cantidad_materias}%"))

    total = query.count()

    column = getattr(Carrera, order_by)

    column = column.desc() if order_dir == "desc" else column.asc()

    items = query.order_by(column).offset(skip).limit(limit).all()

    return {"total": total, "items": items}


def get_carrera_by_id(carrera_id: int, db: Session):

    db_carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()

    if db_carrera is None:
        raise HTTPException(status_code=404, detail="Carrera not found")

    return db_carrera


def update_carrera(carrera_data: CarreraUpdate, carrera_id: int, db: Session):

    db_carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()

    if db_carrera is None:
        raise HTTPException(status_code=404, detail="Carrera not found")

    for key, value in carrera_data.model_dump(exclude=True).items():
        setattr(db_carrera, key, value)

    db.commit()
    db.refresh(db_carrera)
    return db_carrera


def delete_carrera(carrera_id: int, db: Session):

    db_carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()

    if db_carrera is None:
        raise HTTPException(status_code=404, detail="Carrera not found")

    db.delete(db_carrera)
    db.commit()
    return db_carrera
