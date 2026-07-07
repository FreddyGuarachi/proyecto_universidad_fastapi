from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.alumno import Alumno
    from app.models.docente import Docente


class Carrera(Base):
    __tablename__ = "carreras"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=False)
    titulo_otorgado: Mapped[str] = mapped_column(nullable=False)
    cantidad_materias: Mapped[int] = mapped_column(nullable=False)

    alumnos: Mapped[list[Alumno]] = relationship(back_populates="carrera")
    docentes: Mapped[list[Docente]] = relationship(back_populates="carrera")
