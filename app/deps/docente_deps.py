from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.docente import DocenteService


def get_docente_service(db: Session = Depends(get_db)) -> DocenteService:
    return DocenteService(db)


DocenteServiceDep = Annotated[DocenteService, Depends(get_docente_service)]
