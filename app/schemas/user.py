from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    nomeCompleto: str
    matricula: str
    email: EmailStr
    curso: str
    tipoAcesso: str
    cargoEquipe: Optional[str] = None
    equipeId: Optional[int] = None

class UserCreate(UserBase):
    password: str
    dataInicio: date
    ativo: bool = True

class UserUpdate(BaseModel):
    nomeCompleto: Optional[str] = None
    matricula: Optional[str] = None
    email: Optional[EmailStr] = None
    curso: Optional[str] = None
    tipoAcesso: Optional[str] = None
    cargoEquipe: Optional[str] = None
    equipeId: Optional[int] = None
    password: Optional[str] = None
    ativo: Optional[bool] = None

class UserOut(UserBase):
    id: int
    dataInicio: date
    ativo: bool

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut