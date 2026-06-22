from typing import Optional, Literal

from fastapi import APIRouter, Query, Path, Depends

from app.deps.docente_deps import DocenteServiceDep
from app.schemas import docente
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/docentes", tags=["Docentes"], dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=docente.DocenteResponse)
def create_docente(
    service: DocenteServiceDep,
    docente_data: docente.DocenteCreate,
):
    return service.create(docente_data)


@router.get("/", response_model=docente.DocenteListResponse)
def get_docentes(
    service: DocenteServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    name: Optional[str] = Query(None, min_length=1, max_length=100),
    matricula: Optional[str] = Query(None, min_length=1, max_length=50),
    dni: Optional[str] = Query(None, min_length=1, max_length=50),
    email: Optional[str] = Query(None),
    order_by: Literal["name", "matricula", "dni", "email"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
):
    return service.find_all(
        skip=skip,
        limit=limit,
        name=name,
        matricula=matricula,
        dni=dni,
        email=email,
        order_by=order_by,
        order_dir=order_dir,
    )


@router.get("/{docente_id}", response_model=docente.DocenteResponse)
def get_docente_by_id(service: DocenteServiceDep, docente_id: int = Path(..., ge=1)):

    return service.find_by_id(docente_id)


@router.put("/{docente_id}", response_model=docente.DocenteResponse)
def update_docente(
    service: DocenteServiceDep,
    docente_data: docente.DocenteUpdate,
    docente_id: int = Path(..., ge=1),
):

    return service.update(docente_data=docente_data, docente_id=docente_id)


@router.delete("/{docente_id}", response_model=docente.DocenteResponse)
def delete_docente(service: DocenteServiceDep, docente_id: int = Path(..., ge=1)):

    return service.delete(docente_id)
