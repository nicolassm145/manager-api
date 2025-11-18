from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    nome: str
    sku: str
    categoria: str
    quantidade: int
    localizacao: str
    equipeId: Optional[int] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[str] = None
    quantidade: Optional[int] = None
    localizacao: Optional[str] = None

class ItemOut(ItemBase):
    id: int

    class Config:
        from_attributes = True