from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.services.user_service import get_user_by_email
from app.utils.security import verifyPassword, createAcessToken

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verifyPassword(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token_data = {"id": user.id, "role": user.role}
    access_token = createAcessToken(token_data)
    return {"access_token": access_token, "token_type": "bearer"}


