from fastapi import (
    APIRouter,
    Query,
    Path,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session
from typing import Optional, Literal
from app.db.database import get_db
from app.schemas.alumno import (
    AlumnoCreate,
    AlumnoUpdate,
    AlumnoResponse,
    AlumnoListResponse,
)
from app.crud.alumno import (
    create_alumno as create_alumno_router,
    get_alumnos as get_alumnos_router,
    get_alumno_by_id as get_alumno_by_id_router,
    update_alumno as update_alumno_router,
    delete_alumno as delete_alumno_router,
    upload_image_alumno as upload_image_alumno_router,
)
from app.auth.security import get_current_user
from app.services.file_service import save_image

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.post("/", response_model=AlumnoResponse)
def create_alumno(
    alumno_data: AlumnoCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):

    return create_alumno_router(alumno_data=alumno_data, db=db)


@router.post("/{alumno_id}/image")
async def upload_image_alumno(
    alumno_id: int = Path(..., ge=1),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    image_path = await save_image(file=file, alumno_id=alumno_id)

    upload_image_alumno_router(db=db, alumno_id=alumno_id, image_path=image_path)

    return {"message": "imagen guardada"}


@router.get("/", response_model=AlumnoListResponse)
def get_alumnos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    name: Optional[str] = Query(None, min_length=1, max_length=100),
    dni: Optional[str] = Query(None, min_length=1, max_length=50),
    email: Optional[str] = Query(None),
    order_by: Literal["name", "dni", "email"] = "name",
    order_dir: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
):
    return get_alumnos_router(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        dni=dni,
        email=email,
        order_by=order_by,
        order_dir=order_dir,
    )


@router.get("/{alumno_id}", response_model=AlumnoResponse)
def get_alumno_by_id(alumno_id: int = Path(..., ge=1), db: Session = Depends(get_db)):

    return get_alumno_by_id_router(alumno_id=alumno_id, db=db)


@router.put("/{alumno_id}", response_model=AlumnoResponse)
def update_alumno(
    alumno_data: AlumnoUpdate,
    alumno_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):

    return update_alumno_router(alumno_data=alumno_data, alumno_id=alumno_id, db=db)


@router.delete("/{alumno_id}", response_model=AlumnoResponse)
def delete_alumno(alumno_id: int = Path(..., ge=1), db: Session = Depends(get_db)):

    return delete_alumno_router(alumno_id=alumno_id, db=db)
