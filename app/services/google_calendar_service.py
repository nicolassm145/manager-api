from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from app.models.equipe_drive import EquipeDriveIntegration
from app.utils.crypto import decrypt_token
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.config import settings
from google.auth.transport.requests import Request

SCOPES = settings.GOOGLE_SCOPES.split(",")

def build_calendar_service_from_creds(creds: Credentials):
    return build('calendar', 'v3', credentials=creds)

def get_or_create_team_calendar(drive_service, calendar_service, equipe_nome: str):
    """
    Procura um calendário chamado LeagueManager_<Equipe> e cria caso não exista.
    """

    search_name = f"LeagueManager_{equipe_nome}"

    calendar_list = calendar_service.calendarList().list().execute()
    for cal in calendar_list.get("items", []):
        if cal.get("summary") == search_name:
            return cal["id"]

    # Criar novo calendário
    calendar_body = {
        "summary": search_name,
        "timeZone": "America/Sao_Paulo"
    }

    new_calendar = calendar_service.calendars().insert(body=calendar_body).execute()

    # Adicionar à lista de calendários do usuário
    calendar_service.calendarList().insert(body={"id": new_calendar["id"]}).execute()

    return new_calendar["id"]


def create_event(calendar_service, calendar_id, event_data: dict):
    event = calendar_service.events().insert(
        calendarId=calendar_id,
        body=event_data
    ).execute()
    return event


def list_events(calendar_service, calendar_id):
    now = datetime.utcnow().isoformat() + "Z"
    events = calendar_service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    return events.get("items", [])


def update_event(calendar_service, calendar_id, event_id, data):
    updated_event = calendar_service.events().patch(
        calendarId=calendar_id,
        eventId=event_id,
        body=data
    ).execute()
    return updated_event


def delete_event(calendar_service, calendar_id, event_id):
    calendar_service.events().delete(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()
    return True

