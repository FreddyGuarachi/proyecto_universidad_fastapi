from fastapi import APIRouter, Query, Path, Depends
from sqlalchemy.orm import Session
from typing import Optional, Literal
from app.db.database import get_db
from app.schemas.carrera import (
    CarreraCreate,
    CarreraUpdate,
    CarreraResponse,
    CarreraListResponse,
)
from app.crud.carrera import (
    create_carrera as create_carrera_router,
    get_carreras as get_carreras_router,
    get_carrera_by_id as get_carrera_by_id_router,
    update_carrera as update_carrera_router,
    delete_carrera as delete_carrera_router,
)

router = APIRouter(prefix="/carreras", tags=["Carreras"])


@router.post("/", response_model=CarreraResponse)
def create_carrera(carrera_data: CarreraCreate, db: Session = Depends(get_db)):

    return create_carrera_router(carrera_data=carrera_data, db=db)


@router.get("/", response_model=CarreraListResponse)
def get_carreras(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    name: Optional[str] = Query(None, min_length=1, max_length=100),
    titulo_otorgado: Optional[str] = Query(None, min_length=1, max_length=100),
    cantidad_materias: Optional[int] = Query(None, ge=1),
    order_by: Literal["name", "titulo_otorgado", "cantidad_materias"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
):
    return get_carreras_router(
        skip=skip,
        limit=limit,
        name=name,
        titulo_otorgado=titulo_otorgado,
        cantidad_materias=cantidad_materias,
        order_by=order_by,
        order_dir=order_dir,
        db=db,
    )


@router.get("/{carrera_id}", response_model=CarreraResponse)
def get_carrera_by_id(carrera_id: int = Path(..., ge=1), db: Session = Depends(get_db)):

    return get_carrera_by_id_router(carrera_id=carrera_id, db=db)


@router.put("/{carrera_id}", response_model=CarreraResponse)
def update_carrera(
    carrera_data: CarreraUpdate,
    carrera_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):

    return update_carrera_router(
        carrera_data=carrera_data, carrera_id=carrera_id, db=db
    )


@router.delete("/{carrera_id}", response_model=CarreraResponse)
def delete_carrera(
    carrera_id: int = Path(..., ge=1), db: Session = Depends(get_db)
):

    return delete_carrera_router(carrera_id=carrera_id, db=db)
