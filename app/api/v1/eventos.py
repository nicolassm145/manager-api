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

@router.get("/{eventoId}/participantes")
def get_participantes(eventoId: int, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    return list_participantes(db, eventoId)

@router.post("/{eventoId}/participar")
def participar_evento(
    eventoId: int,
    data: EventoParticipanteBase,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    return add_participante(db, eventoId, current_user.id, data.status)

@router.patch("/participantes/{participanteId}")
def update_participante_route(
    participanteId: int,
    data: EventoParticipanteBase,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    return update_participante(db, participanteId, data.status, data.observacao)


#TAREFAS
@router.get("/{eventoId}/tarefas")
def get_tarefas(eventoId: int, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    return list_tarefas(db, eventoId)


@router.post("/{eventoId}/tarefas")
def add_tarefa_route(
    eventoId: int,
    data: EventoTarefaBase,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    return add_tarefa(db, eventoId, data.membroId, data.descricao)


@router.patch("/tarefas/{tarefaId}")
def update_tarefa_route(
    tarefaId: int,
    data: EventoTarefaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    return update_tarefa(db, tarefaId, data.descricao, data.concluida)