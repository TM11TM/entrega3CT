from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from app import crud, schemas
from app.db import SessionLocal, engine, Base
import logging

Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# bbdd error
try:
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
    logger.info("Conexión a la base de datos exitosa")
except OperationalError as e:
    logger.error(f"No se pudo conectar a la base de datos: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/estudiante", response_model=list[schemas.EstudianteResponse])
def listar_estudiantes(db: Session = Depends(get_db)):
    logger.info("Listando todos los estudiantes")
    estudiantes = crud.get_estudiantes(db)
    if estudiantes is None:
        raise HTTPException(status_code=404, detail="No se encontraron estudiantes")
    return estudiantes

@app.get("/estudiante/{estudiante_id}", response_model=schemas.EstudianteResponse)
def obtener_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    logger.info(f"Obteniendo estudiante con id {estudiante_id}")
    estudiante = crud.get_estudiante(db, estudiante_id)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@app.post("/estudiante", response_model=schemas.EstudianteResponse, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: schemas.EstudianteCreate, db: Session = Depends(get_db)):
    logger.info(f"Creando estudiante: {estudiante}")
    # Validaciones manuales (adicionales a las del crud)
    if not estudiante.nombre or not estudiante.apellidos or not estudiante.master or not estudiante.telefono or not estudiante.email:
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios")
    return crud.create_estudiante(db, estudiante)

@app.delete("/estudiante/{estudiante_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    logger.info(f"Eliminando estudiante con id {estudiante_id}")
    estudiante = crud.get_estudiante(db, estudiante_id)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    crud.delete_estudiante(db, estudiante_id)
    return None