from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.evento import Evento, EventoParticipante, EventoTarefa
from app.schemas.evento import EventoCreate, EventoUpdate
from datetime import datetime

def create_evento(db: Session, equipeId: int, googleEventId: str, data: EventoCreate):
    evento = Evento(
        equipeId=equipeId,
        googleEventId=googleEventId,
        titulo=data.titulo,
        descricao=data.descricao,
        startDatetime=data.startDatetime,
        endDatetime=data.endDatetime,
    )
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

def update_evento(db: Session, eventoId: int, data: EventoUpdate):
    evento = db.query(Evento).filter(Evento.id == eventoId).first()

    if not evento:
        raise HTTPException(404, "Evento não encontrado")

    for attr, value in data.dict(exclude_unset=True).items():
        setattr(evento, attr, value)

    db.commit()
    db.refresh(evento)
    return evento

def delete_evento(db: Session, eventoId: int):
    evento = db.query(Evento).filter(Evento.id == eventoId).first()

    if not evento:
        raise HTTPException(404, "Evento não encontrado")

    db.delete(evento)
    db.commit()
    return True


def add_participante(db: Session, eventoId: int, membroId: int, status: str):
    participante = EventoParticipante(
        eventoId=eventoId,
        membroId=membroId,
        status=status
    )

    db.add(participante)
    db.commit()
    db.refresh(participante)
    return participante

def update_participante(db: Session, participanteId: int, status: str, observacao: str):
    part = db.query(EventoParticipante).filter(EventoParticipante.id == participanteId).first()

    if not part:
        raise HTTPException(404, "Participante não encontrado")

    part.status = status
    part.observacao = observacao
    part.updatedAt = datetime.utcnow()

    db.commit()
    db.refresh(part)
    return part

def list_participantes(db: Session, eventoId: int):
    return db.query(EventoParticipante).filter(
        EventoParticipante.eventoId == eventoId
    ).all()

def add_tarefa(db: Session, eventoId: int, membroId: int, descricao: str):
    tarefa = EventoTarefa(
        eventoId=eventoId,
        membroId=membroId,
        descricao=descricao
    )

    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa


def update_tarefa(db: Session, tarefaId: int, descricao: str, concluida: bool):
    tarefa = db.query(EventoTarefa).filter(EventoTarefa.id == tarefaId).first()

    if not tarefa:
        raise HTTPException(404, "Tarefa não encontrada")

    if descricao:
        tarefa.descricao = descricao

    if concluida is not None:
        tarefa.concluido = concluida

    tarefa.updatedAt = datetime.utcnow()

    db.commit()
    db.refresh(tarefa)
    return tarefa

def list_tarefas(db: Session, eventoId: int):
    return db.query(EventoTarefa).filter(
        EventoTarefa.eventoId == eventoId
    ).all()

