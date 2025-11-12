from pydantic import BaseModel
from datetime import date

class TransacaoBase(BaseModel):
    descricao: str
    valor: float
    data: date
    tipo: str
    categoria: str
    equipeId: int

class TransacaoCreate(TransacaoBase):
    pass

class TransacaoOut(TransacaoBase):
    id: int
    criadoPor: int

    class Config:
        from_attributes = True