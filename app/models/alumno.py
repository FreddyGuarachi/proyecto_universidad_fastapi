from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.carrera import Carrera


class Alumno(Base):
    __tablename__ = "alumnos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    dni: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    foto_perfil: Mapped[str | None] = mapped_column(nullable=True)

    carrera_id: Mapped[int] = mapped_column(ForeignKey("carreras.id"))
    carrera: Mapped[Carrera] = relationship(back_populates="alumnos")
