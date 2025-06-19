from pydantic import BaseModel, Field

class Estudiante(BaseModel):
    nombre: str = Field( description="Nombre del estudiante")
    apellidos: str = Field( description="Apellidos del estudiante")
    master: str = Field( description="Nombre del máster que estudia")
    telefono: str = Field( description="Teléfono español de 9 dígitos")
    email:str = Field(description="Correo electrónico del estudiante")


class EstudianteCreate(Estudiante):
    pass


class EstudianteResponse(Estudiante):
    id: int

    class Config:
        orm_mode = True
 