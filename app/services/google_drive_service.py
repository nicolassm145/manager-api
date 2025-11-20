from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from app.utils.crypto import encrypt_token, decrypt_token
from app.models.equipe_drive import EquipeDriveIntegration
from sqlalchemy.orm import Session
from app.core.config import settings
from google.auth.transport.requests import Request

SCOPES = settings.GOOGLE_SCOPES.split(",")

def build_flow():
    return Flow.from_client_config(
        {
            'web': {
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
            }
        },
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI
    )

def get_authorize_url(state: str = None) -> str:
    flow = build_flow()
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',
        state=state
    )
    return auth_url

def exchange_code_for_tokens(code: str):
    flow = build_flow()
    flow.fetch_token(code=code)
    return flow.credentials

def build_drive_service_from_creds(creds: Credentials):
    return build('drive', 'v3', credentials=creds)

def refresh_and_get_credentials(db: Session, integration: EquipeDriveIntegration) -> Credentials:
    refresh_token = decrypt_token(integration.refreshToken)
    access_token = decrypt_token(integration.accessToken) if integration.accessToken else None

    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
    )

    if not creds.valid or creds.expired:
        creds.refresh(Request())

    integration.accessToken = encrypt_token(creds.token)

    if creds.refresh_token:
        integration.refreshToken = encrypt_token(creds.refresh_token)

    if creds.expiry:
        integration.tokenExpiresAt = creds.expiry

    db.add(integration)
    db.commit()
    db.refresh(integration)

    return creds