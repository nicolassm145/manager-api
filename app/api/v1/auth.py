from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.utils.security import verifyPassword, createAcessToken
from fastapi import status
from app.models.user import User
from app.schemas.user import LoginResponse, UserOut
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=LoginResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verifyPassword(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    
    # Verificar se o usuário está ativo
    if not user.ativo:
        raise HTTPException(status_code=401, detail="Usuário desativado")
    
    token_data = {"id": user.id, "role": user.tipoAcesso}
    access_token = createAcessToken(token_data)
    
    # Converter o usuário para o schema UserOut
    user_out = UserOut.model_validate(user)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_out
    }


