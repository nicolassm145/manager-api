from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import getCurrentUser
from app.models.equipe import Equipe
from app.services.google_drive_service import get_authorize_url, exchange_code_for_tokens, build_drive_service_from_creds, refresh_and_get_credentials
from app.utils.crypto import encrypt_token
from app.models.equipe_drive import EquipeDriveIntegration
from datetime import datetime

router = APIRouter(prefix="/api/v1/google-drive", tags=["Google Drive"])

#Endpoint para autorização do Google Drive
@router.get('/authorize')
def authorize(equipeId: int, db: Session = Depends(get_db), current_user = Depends(getCurrentUser)):
    if current_user.tipoAcesso != 'Líder':
        raise HTTPException(status_code=403, detail='Apenas líderes podem conectar a conta do Drive')

    equipe = db.query(Equipe).filter(Equipe.id == equipeId).first()
    if not equipe:
        raise HTTPException(status_code=404, detail='Equipe não encontrada')

    url = get_authorize_url(state=str(equipeId))
    return {"url": url}

#Callback endpoint após autorização do Google Drive

from fastapi.responses import RedirectResponse
from app.core.config import settings

@router.get('/callback')
def oauth_callback(code: str, state: str, db: Session = Depends(get_db)):
    equipeId = int(state)
    equipe = db.query(Equipe).filter(Equipe.id == equipeId).first()
    if not equipe:
        raise HTTPException(404, 'Equipe não encontrada')

    creds = exchange_code_for_tokens(code)
    drive = build_drive_service_from_creds(creds)

    folder_metadata = {
        'name': f"LeagueManager_{equipe.nome}",
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive.files().create(body=folder_metadata, fields='id').execute()

    from app.models.equipe_drive import EquipeDriveIntegration
    integration = db.query(EquipeDriveIntegration).filter(
        EquipeDriveIntegration.equipeId == equipeId
    ).first()
    if not integration:
        integration = EquipeDriveIntegration(equipeId=equipeId)

    integration.driveFolderId = folder['id']
    integration.accessToken = encrypt_token(creds.token)
    integration.refreshToken = encrypt_token(creds.refresh_token or '')
    integration.tokenExpiresAt = creds.expiry

    db.add(integration)
    db.commit()
    db.refresh(integration)

    # Redireciona para o frontend após sucesso
    redirect_url = f"{settings.FRONTEND_URL}/files"
    return RedirectResponse(url=redirect_url, status_code=302)

# ENdopoint para listar arquivos na pasta do Google Drive da equipe
@router.get('/files')
def list_files(db: Session = Depends(get_db), current_user = Depends(getCurrentUser)):
    integration = db.query(EquipeDriveIntegration).filter(EquipeDriveIntegration.equipeId == current_user.equipeId).first()
    if not integration:
        raise HTTPException(status_code=404, detail='Equipe não possui Drive vinculado')
    
    creds = refresh_and_get_credentials(db, integration)
    drive = build_drive_service_from_creds(creds)

    query = f"'{integration.driveFolderId}' in parents and trashed = false"
    results = drive.files().list(q=query, fields='files(id,name,mimeType,size,modifiedTime,webViewLink)').execute()
    return results.get('files', [])

#Endpoint para fazer upload de arquivo na pasta do Google Drive da equipe - Apenas Lider
@router.post('/upload')
async def upload_file(equipeId: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(getCurrentUser)):
    # Log para debug: checar se arquivo chegou
    if not file:
        raise HTTPException(status_code=400, detail='Arquivo não enviado (campo file ausente)')
    if not equipeId:
        raise HTTPException(status_code=400, detail='equipeId não enviado')
    integration = db.query(EquipeDriveIntegration).filter(EquipeDriveIntegration.equipeId == equipeId).first()
    if not integration:
        raise HTTPException(status_code=404, detail='Integração não encontrada')

    if current_user.tipoAcesso.lower() == 'lider' and current_user.equipeId != equipeId:
        raise HTTPException(status_code=403, detail='Líder só pode enviar arquivos para sua própria equipe')
    
    creds = refresh_and_get_credentials(db, integration)
    drive = build_drive_service_from_creds(creds)

    content = await file.read()
    from googleapiclient.http import MediaInMemoryUpload
    media = MediaInMemoryUpload(content, mimetype=file.content_type)

    body = { 'name': file.filename, 'parents': [integration.driveFolderId] }
    uploaded = drive.files().create(body=body, media_body=media, fields='id').execute()


    return { 'fileId': uploaded.get('id') }

@router.get('/download/{file_id}')
def download_file(file_id: str, db: Session = Depends(get_db), current_user = Depends(getCurrentUser)):
    integration = db.query(EquipeDriveIntegration).filter(EquipeDriveIntegration.equipeId == current_user.equipeId).first()
    if not integration:
        raise HTTPException(status_code=404, detail='Integração não encontrada')

    creds = refresh_and_get_credentials(db, integration)
    drive = build_drive_service_from_creds(creds)

    try:
        request = drive.files().get_media(fileId=file_id)
        data = request.execute()
    except Exception:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={file_id}"
        }
    )

#Endpoint para deletar arquivo
@router.delete('/delete/{file_id}')
def delete_file(file_id: str, db: Session = Depends(get_db), current_user = Depends(getCurrentUser)):
    integration = db.query(EquipeDriveIntegration).filter(EquipeDriveIntegration.equipeId == current_user.equipeId).first()
    if not integration:
        raise HTTPException(status_code=404, detail='Integração não encontrada')

    creds = refresh_and_get_credentials(db, integration)
    drive = build_drive_service_from_creds(creds)

    try:
        drive.files().delete(fileId=file_id).execute()
    except Exception:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado ou não pode ser deletado")
    
    return {"detail": "Arquivo deletado com sucesso"}