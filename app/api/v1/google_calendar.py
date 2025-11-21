from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import getCurrentUser
from app.models.equipe import Equipe
from app.models.equipe_drive import EquipeDriveIntegration

from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoUpdate
from app.services.evento_service import create_evento, update_evento, delete_evento
from app.services.google_drive_service import refresh_and_get_credentials
from app.services.google_calendar_service import (
    build_calendar_service_from_creds,
    get_or_create_team_calendar,
    create_event,
    update_event,
    delete_event
)

router = APIRouter(prefix="api/v1/google_calendar", tags=["Google Calendar"])

@router.post("/eventos")
def create_calendar_event(evento: EventoCreate, db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    
    if current_user.tipoAcesso.lower() != "líder":
        raise HTTPException(403, "Acesso negado. Apenas líderes podem criar eventos no Google Calendar.")
    
    integration = db.query(EquipeDriveIntegration).filter(
        EquipeDriveIntegration.equipeId == current_user.equipeId
    ).first()

    if not integration:
        raise HTTPException(400, "Integração com Google não encontrada para a equipe.")
    
    creds = refresh_and_get_credentials(db, integration)
    calendar_service = build_calendar_service_from_creds(creds)

    equipe = db.query(Equipe).filter(Equipe.id == current_user.equipeId).first()
    calendar_id = get_or_create_team_calendar(None, calendar_service, equipe.nome)

    google_event = {
        "summary": evento.titulo,
        "description": evento.descricao,
        "start": {
            "dateTime": evento.startDateTime.isoformat(),
            "timeZone": "America/Sao_Paulo"
        },
        "end": {
            "dateTime": evento.endDateTime.isoformat(),
            "timeZone": "America/Sao_Paulo"
        }
    }

    created_google_event = create_event(calendar_service, calendar_id, google_event)

    evento_db = create_evento(
        db,
        equipeId=current_user.equipeId,
        googleEventId=created_google_event["id"],
        data=evento
    )

    return evento_db


@router.patch("/events/{event_id}")
def update_calendar_event(
    event_id: int,
    data: EventoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    if current_user.tipoAcesso.lower() != "líder":
        raise HTTPException(403, "Somente líderes podem editar eventos")

    evento = db.query(Evento).filter(Evento.id == event_id).first()
    if not evento:
        raise HTTPException(404, "Evento não encontrado")

    integration = db.query(EquipeDriveIntegration).filter(
        EquipeDriveIntegration.equipeId == evento.equipeId
    ).first()

    creds = refresh_and_get_credentials(db, integration)
    calendar_service = build_calendar_service_from_creds(creds)

    # Atualiza no banco
    updated = update_evento(db, event_id, data)

    # Atualiza no Google
    google_data = {}

    if data.titulo:
        google_data["summary"] = data.titulo
    if data.descricao:
        google_data["description"] = data.descricao
    if data.startDateTime:
        google_data.setdefault("start", {})["dateTime"] = data.startDateTime.isoformat()
        google_data["start"]["timeZone"] = "America/Sao_Paulo"
    if data.endDateTime:
        google_data.setdefault("end", {})["dateTime"] = data.endDateTime.isoformat()
        google_data["end"]["timeZone"] = "America/Sao_Paulo"

    update_event(calendar_service, evento.googleEventId, google_data)

    return updated


@router.delete("/events/{event_id}")
def delete_calendar_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(getCurrentUser)
):
    if current_user.tipoAcesso.lower() != "líder":
        raise HTTPException(403, "Somente líderes podem deletar eventos")

    evento = db.query(Evento).filter(Evento.id == event_id).first()
    if not evento:
        raise HTTPException(404, "Evento não encontrado")

    integration = db.query(EquipeDriveIntegration).filter(
        EquipeDriveIntegration.equipeId == evento.equipeId
    ).first()

    creds = refresh_and_get_credentials(db, integration)
    calendar_service = build_calendar_service_from_creds(creds)

    delete_event(calendar_service, evento.googleEventId)
    delete_evento(db, event_id)

    return {"detail": "Evento deletado com sucesso"}

