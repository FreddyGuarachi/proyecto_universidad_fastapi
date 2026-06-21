from typing import Optional, Literal

from fastapi import APIRouter, Query, Path, Depends

from app.schemas import alumno
from app.deps.alumno_deps import AlumnoServiceDep
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/alumnos", tags=["Alumnos"], dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=alumno.AlumnoResponse)
def create_alumno(
    service: AlumnoServiceDep,
    alumno_data: alumno.AlumnoCreate,
):

    return service.create(alumno_data=alumno_data)


@router.get("/", response_model=alumno.AlumnoListResponse)
def get_alumnos(
    service: AlumnoServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    name: Optional[str] = Query(None, min_length=1, max_length=100),
    dni: Optional[str] = Query(None, min_length=1, max_length=50),
    email: Optional[str] = Query(None),
    order_by: Literal["name", "dni", "email"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
):
    return service.find_all(
        skip=skip,
        limit=limit,
        name=name,
        dni=dni,
        email=email,
        order_by=order_by,
        order_dir=order_dir,
    )


@router.get("/{alumno_id}", response_model=alumno.AlumnoResponse)
def get_alumno_by_id(service: AlumnoServiceDep, alumno_id: int = Path(..., ge=1)):

    return service.find_by_id(alumno_id=alumno_id)


@router.put("/{alumno_id}", response_model=alumno.AlumnoResponse)
def update_alumno(
    service: AlumnoServiceDep,
    alumno_data: alumno.AlumnoUpdate,
    alumno_id: int = Path(..., ge=1),
):

    return service.update(alumno_data=alumno_data, alumno_id=alumno_id)


@router.delete("/{alumno_id}", response_model=alumno.AlumnoResponse)
def delete_alumno(service: AlumnoServiceDep, alumno_id: int = Path(..., ge=1)):

    return service.delete(alumno_id=alumno_id)
