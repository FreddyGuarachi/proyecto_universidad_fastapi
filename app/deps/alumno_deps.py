from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.alumno_service import AlumnoService


def get_alumno_service(db: Session = Depends(get_db)) -> AlumnoService:
    return AlumnoService(db)


AlumnoServiceDep = Annotated[AlumnoService, Depends(get_alumno_service)]
