from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.utils.security import verifyPassword, createAcessToken
from fastapi import status
from app.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verifyPassword(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    token_data = {"id": user.id, "role": user.tipoAcesso}
    access_token = createAcessToken(token_data)
    return {"access_token": access_token, "token_type": "bearer"}


