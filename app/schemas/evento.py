from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Evento Schemas
class EventoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    startDatetime: datetime
    endDatetime: datetime


class EventoCreate(EventoBase):
    pass


class EventoUpdate(EventoBase):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    startDatetime: Optional[datetime] = None
    endDatetime: Optional[datetime] = None


class EventOut(EventoBase):
    id: int
    equipeId: int
    googleEventId: Optional[str] = None
    createdAt: datetime

    class Config:
        from_attributes = True



# Participantes
class EventoParticipanteBase(BaseModel):
    membroId: int
    status: Optional[str] = "pendente"  # pendente, confirmado, recusado
    observacao: Optional[str] = None


class EventoParticipanteCreate(EventoParticipanteBase):
    id: int

    class Config:
        from_attributes = True



#Tarefas
class EventoTarefaBase(BaseModel):
    membroId: int
    descricao: str


class EventoTarefaUpdate(BaseModel):
    descricao: Optional[str] = None
    concluido: Optional[bool] = None


class EventoTarefaOut(EventoTarefaBase):
    id: int
    concluida: bool

    class Config:
        from_attributes = True