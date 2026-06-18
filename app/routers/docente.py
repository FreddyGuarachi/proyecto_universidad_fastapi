from fastapi import APIRouter, Query, Path, Depends
from sqlalchemy.orm import Session
from typing import Optional, Literal
from app.db.database import get_db
from app.schemas.docente import (
    DocenteCreate,
    DocenteUpdate,
    DocenteResponse,
    DocenteListResponse,
)
from app.crud.docente import (
    create_docente as create_docente_router,
    get_docentes as get_docentes_router,
    get_docente_by_id as get_docente_by_id_router,
    update_docente as update_docente_router,
    delete_docente as delete_docente_router,
)
from app.auth.security import get_current_user

router = APIRouter(prefix="/docentes", tags=["Docentes"])


@router.post("/", response_model=DocenteResponse)
def create_docente(
    docente_data: DocenteCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):

    return create_docente_router(docente_data=docente_data, db=db)


@router.get("/", response_model=DocenteListResponse)
def get_docentes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    name: Optional[str] = Query(None, min_length=1, max_length=100),
    matricula: Optional[str] = Query(None, min_length=1, max_length=50),
    dni: Optional[str] = Query(None, min_length=1, max_length=50),
    email: Optional[str] = Query(None),
    order_by: Literal["name", "matricula", "dni", "email"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
):
    return get_docentes_router(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        matricula=matricula,
        dni=dni,
        email=email,
        order_by=order_by,
        order_dir=order_dir,
    )


@router.get("/{docente_id}", response_model=DocenteResponse)
def get_alumno_by_id(docente_id: int = Path(..., ge=1), db: Session = Depends(get_db)):

    return get_docente_by_id_router(docente_id=docente_id, db=db)


@router.put("/{docente_id}", response_model=DocenteResponse)
def update_docente(
    docente_data: DocenteUpdate,
    docente_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):

    return update_docente_router(
        docente_data=docente_data, docente_id=docente_id, db=db
    )


@router.delete("/{docente_id}", response_model=DocenteResponse)
def delete_alumno(docente_id: int = Path(..., ge=1), db: Session = Depends(get_db)):

    return delete_docente_router(docente_id=docente_id, db=db)
