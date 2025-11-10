from pydantic import BaseModel, EmailStr
from datetime import date

class UserBase(BaseModel):
    nomeCompleto: str
    matricula: str
    email: EmailStr
    curso: str
    tipoAcesso: str
    cargoEquipe: str
    equipeId: int

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    dataInicio: date
    ativo: bool

    class Config:
        orm_mode = True