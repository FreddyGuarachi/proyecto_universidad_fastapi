from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.carrera_service import CarreraService


def get_carrera_service(db: Session = Depends(get_db)) -> CarreraService:
    return CarreraService(db)


CarreraServiceDep = Annotated[CarreraService, Depends(get_carrera_service)]
