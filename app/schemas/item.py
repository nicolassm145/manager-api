from pydantic import BaseModel

class ItemBase(BaseModel):
    nome: str
    sku: str
    categoria: str
    quantidade: int
    localizacao: str
    equipeId: int

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int

    class Config:
        orm_mode = True