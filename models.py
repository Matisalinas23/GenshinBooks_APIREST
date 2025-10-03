from sqlmodel import SQLModel, Field, Relationship
from typing import List
from sqlalchemy import ForeignKey

# Modelos de libro
class LibroBase(SQLModel):
    nombre: str

class LibroCreateIn(LibroBase):
    id: str = Field()

class LibroCreateOut(SQLModel):
    id: str = Field()

class Libro(LibroBase, table=True):
    id: str = Field(primary_key=True)
    volumenes: List["Volumen"] = Relationship(back_populates="libro")


# Modelos de volumen

class VolumenBase(SQLModel):
    nombre: str = Field()
    descripcion: str = Field()
    cuerpo: str = Field()

class VolumenCreateIn(VolumenBase):
    id: str = Field()

class VolumenCreateOut(SQLModel):
    id: str = Field()

class Volumen(VolumenBase, table=True):
    id: str = Field(primary_key=True)
    libro_id: str = Field(ForeignKey("libros.id", ondelete="CASCADE"), nullable=False)
    libro: "Libro" = Relationship(back_populates="volumenes")