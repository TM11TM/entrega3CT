from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
import re

def get_estudiantes(db: Session):
    return db.query(models.Estudiante).all()

def get_estudiante(db: Session, estudiante_id: int):
    estudiante = db.query(models.Estudiante).filter(models.Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

def create_estudiante(db: Session, estudiante: schemas.EstudianteCreate):
    # Validación teléfono: 9 dígitos españoles (solo números)
    if not re.fullmatch(r"\d{9}", estudiante.telefono):
        raise HTTPException(status_code=400, detail="Teléfono inválido. Debe tener 9 dígitos numéricos")

    # Validación email básica con regex
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.fullmatch(email_regex, estudiante.email):
        raise HTTPException(status_code=400, detail="Email inválido")

    # Comprobar si email ya existe
    existing = db.query(models.Estudiante).filter(models.Estudiante.email == estudiante.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    nuevo_estudiante = models.Estudiante(
        nombre=estudiante.nombre,
        apellidos=estudiante.apellidos,
        master=estudiante.master,
        telefono=estudiante.telefono,
        email=estudiante.email
    )
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

def delete_estudiante(db: Session, estudiante_id: int):
    estudiante = db.query(models.Estudiante).filter(models.Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(estudiante)
    db.commit()
