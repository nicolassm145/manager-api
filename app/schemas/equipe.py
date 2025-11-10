from pydantic import BaseModel
from datetime import date

class EquipeBase(BaseModel):
    nome: str
    descricao: str

class EquipeCreate(EquipeBase):
    pass

class EquipeOut(EquipeBase):
    id: int
    criadoEm: date

    class Config:
        orm_mode = True