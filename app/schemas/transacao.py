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

class TransacaoUpdate(BaseModel):
    descricao: str | None = None
    valor: float | None = None
    data: date | None = None
    tipo: str | None = None
    categoria: str | None = None

class TransacaoOut(TransacaoBase):
    id: int
    criadoPor: int

    class Config:
        from_attributes = True