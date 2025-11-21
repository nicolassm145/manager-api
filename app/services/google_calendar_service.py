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



