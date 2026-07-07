from typing import Optional, Literal

from fastapi import APIRouter, Query, Path, Depends

from app.schemas import carrera
from app.deps.carrera_deps import CarreraServiceDep
from app.auth.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/carreras", tags=["Carreras"], dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=carrera.CarreraResponse)
def create_carrera(
    service: CarreraServiceDep,
    carrera_data: carrera.CarreraCreate,
):

    return service.create(carrera_data)


@router.get("/", response_model=carrera.CarreraListResponse)
def get_carreras(
    service: CarreraServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    name: Optional[str] = Query(None, min_length=1, max_length=100),
    titulo_otorgado: Optional[str] = Query(None, min_length=1, max_length=100),
    cantidad_materias: Optional[int] = Query(None, ge=1),
    order_by: Literal["name", "titulo_otorgado", "cantidad_materias"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
):
    return service.find_all(
        skip=skip,
        limit=limit,
        name=name,
        titulo_otorgado=titulo_otorgado,
        cantidad_materias=cantidad_materias,
        order_by=order_by,
        order_dir=order_dir,
    )


@router.get("/{carrera_id}", response_model=carrera.CarreraResponse)
def get_carrera_by_id(service: CarreraServiceDep, carrera_id: int = Path(..., ge=1)):

    return service.find_by_id(carrera_id)


@router.put("/{carrera_id}", response_model=carrera.CarreraResponse)
def update_carrera(
    service: CarreraServiceDep,
    carrera_data: carrera.CarreraUpdate,
    carrera_id: int = Path(..., ge=1),
):

    return service.update(carrera_data=carrera_data, carrera_id=carrera_id)


@router.delete("/{carrera_id}", response_model=carrera.CarreraResponse)
def delete_carrera(service: CarreraServiceDep, carrera_id: int = Path(..., ge=1)):

    return service.delete(carrera_id)
