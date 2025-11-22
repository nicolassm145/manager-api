from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import getCurrentUser
from app.core.database import get_db
from app.models.evento import Evento
from app.schemas.evento import (
    EventoParticipanteBase,
    EventoTarefaBase,
    EventoTarefaUpdate
)
from app.services.evento_service import (
    list_participantes,
    add_participante,
    update_participante,
    list_tarefas,
    add_tarefa,
    update_tarefa
)

router = APIRouter(prefix="/api/v1/eventos", tags=["Eventos"])

#PARTICIPANTES

@router.get("/{googleEventId}/participantes")
def get_participantes(googleEventId: str, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    evento = db.query(Evento).filter(Evento.googleEventId == googleEventId).first()
    if not evento:
        raise HTTPException(404, "Evento não encontrado")
    return list_participantes(db, evento.id)

@router.post("/{googleEventId}/participar")
def participar_evento(
    googleEventId: str,
    data: EventoParticipanteBase,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    evento = db.query(Evento).filter(Evento.googleEventId == googleEventId).first()
    if not evento:
        raise HTTPException(404, "Evento não encontrado")
    return add_participante(db, evento.id, data.membroId, data.status)

@router.patch("/participantes/{participanteId}")
def update_participante_route(
    participanteId: int,
    data: EventoParticipanteBase,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    return update_participante(db, participanteId, data.status, data.observacao)


#TAREFAS
@router.get("/{googleEventId}/tarefas")
def get_tarefas(googleEventId: str, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    evento = db.query(Evento).filter(Evento.googleEventId == googleEventId).first()
    if not evento:
        raise HTTPException(404, "Evento não encontrado")
    return list_tarefas(db, evento.id)


@router.post("/{googleEventId}/tarefas")
def add_tarefa_route(
    googleEventId: str,
    data: EventoTarefaBase,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    evento = db.query(Evento).filter(Evento.googleEventId == googleEventId).first()
    if not evento:
        raise HTTPException(404, "Evento não encontrado")
    return add_tarefa(db, evento.id, data.membroId, data.descricao)


@router.patch("/tarefas/{tarefaId}")
def update_tarefa_route(
    tarefaId: int,
    data: EventoTarefaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    return update_tarefa(db, tarefaId, data.descricao, data.concluido)