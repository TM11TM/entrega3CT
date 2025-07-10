# models.py
from sqlalchemy import Column, Integer, String
from db import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    master = Column(String(100), nullable=False)
    telefono = Column(String(9), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
