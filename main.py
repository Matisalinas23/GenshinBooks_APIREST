from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # "https://midominio.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class Volumen(BaseModel):
    id: str = None
    nombre: str
    cuerpo: str
    descripcion: str

class Libro(BaseModel): 
    id: str = None
    nombre: str
    volumenes: List[Volumen] = []


# Base de datos simulada
genshin_libros_db = []


#Libros

@app.get("/libros", response_model=List[Libro])
def obtener_libros():
    return genshin_libros_db

@app.post("/libros", response_model=Libro)
def crear_libros(libro: Libro):
    if len(libro.volumenes) == 0:
        raise HTTPException(status_code=400, detail="Es obligatorio crear al menos un volumen por libro")
    
    libro.id = str(uuid.uuid4())
    for volumen in libro.volumenes:
        volumen.id = str(uuid.uuid4())

    genshin_libros_db.append(libro)
    
    return libro

@app.get("/libros/{libro_name}", response_model=Libro)
def obtener_libros(libro_name: str):
    libro = next((libro for libro in genshin_libros_db if libro.nombre == libro_name), None)
    if libro is None:
        raise HTTPException(status_code=404, detail='Libro no encontrado')
    return libro

@app.put("/libros/{libro_id}", response_model=Libro)
def actualizar_libro(libro_id: str, libro_actualizado: Libro):
    libro = next((libro for libro in genshin_libros_db if libro.id == libro_id), None)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro_actualizado.id = libro_id

    volumenes_finales = []
    for vol in libro_actualizado.volumenes:
        volumen_existente = None

        if vol.id:
            volumen_existente = next((v for v in libro.volumenes if v.id == vol.id), None)
        else:
            volumen_existente = next((v for v in libro.volumenes if v.nombre == vol.nombre), None)

        if volumen_existente:
            vol.id = volumen_existente.id
        else:
            vol.id = str(uuid.uuid4())

        volumenes_finales.append(vol)

    libro_actualizado.volumenes = volumenes_finales

    index = genshin_libros_db.index(libro)
    genshin_libros_db[index] = libro_actualizado
    return libro_actualizado

@app.delete("/libros/{libro_id}", response_model=Libro)
def eliminar_libros(libro_id: str):
    libro = next((libro for libro in genshin_libros_db if libro.id == libro_id), None)
    if libro is None:
        raise HTTPException(status_code=404, detail='Libro no encontrado')
    genshin_libros_db.remove(libro)
    return libro

@app.get("/libros/{libro_name}/volumenes", response_model=List[Volumen])
def obtener_volumenes(libro_name: str):
    libro: Libro = next((libro for libro in genshin_libros_db if libro.nombre == libro_name), None)
    if libro is None:
        raise HTTPException(status_code=404, detail='Libro no encontrado')
    return libro.volumenes