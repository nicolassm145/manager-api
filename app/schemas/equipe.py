from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from app.schemas.user import UserOut

class EquipeBase(BaseModel):
    nome: str
    descricao: str

class EquipeCreate(EquipeBase):
    pass

class EquipeUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class EquipeOut(EquipeBase):
    id: int
    criadoEm: date
    membros: Optional[List[UserOut]] = None

    class Config:
        from_attributes = True