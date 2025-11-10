from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import user
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserBase, UserUpdate
from app.services.user_service import create_user, get_user, list_users
from app.api.deps import getCurrentUser, requireTipoAcesso, checkUserAccess
from app.utils.security import hash_password
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/api/v1/users", tags=["Usuários"])

# Endpoint para criar um novo usuário
@router.post("/criar", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(user_in: UserCreate, db: Session = Depends(get_db), current_user = Depends(requireTipoAcesso("Administrador", "Líder"))):
    try:
        user = create_user(db, user_in=user_in)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return user


# Listar usuarios - apenas administradores podem listar todos os usuários
@router.get("/listarTudo", response_model=List[UserOut])
def list_users_endpoint(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), current_user = Depends(requireTipoAcesso("Administrador"))):
    users = list_users(db, skip=skip, limit=limit)
    return users 

# Obter usuarios por ID - Administradores, Lideres e Membros da propia equipe podem acessar
@router.get("/listar/{user_id}", response_model=UserOut)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user = Depends(getCurrentUser)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    checkUserAccess(current_user, user)
    return user

# Update de dados do usuario
@router.put("/atualizar/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db), current_user = Depends(getCurrentUser)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Regra 1 - Admin
    if current_user.tipoAcesso == "Administrador":
        for field, value in user_in.model_dump(exclude_unset=True).items():
            if(field == "password" and value):
                user.hashed_password = hash_password(value)
            elif field != "password":
                setattr(user, field, value)

    # Regra 2 - Líder
    elif current_user.tipoAcesso == "Líder":
        if current_user.equipeId != user.equipeId:
            raise HTTPException(status_code=403, detail="Líder não pode alterar usuários de outra equipe")
        for field, value in user_in.model_dump(exclude_unset=True).items():
            if field == "password" and value:
                user.hashed_password = hash_password(value)
            elif field != "password":
                setattr(user, field, value)

    # Regra 3 - Membro
    elif current_user.tipoAcesso == "Membro":
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Membros só podem atualizar seus próprios dados")
        camposPermitidos = {"email", "password"}
        for field, value in user_in.model_dump(exclude_unset=True).items():
            if field not in camposPermitidos:
                continue
            if field == "password" and value:
                user.hashed_password = hash_password(value)
            elif field == "email":
                user.email = value
    
    else:
        raise HTTPException(status_code=403, detail="Permissão negada")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Delatar usuario - Lider e Admin
@router.delete("/deletar/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user = Depends(requireTipoAcesso("Administrador", "Líder"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if current_user.tipoAcesso == "Líder" and current_user.equipeId != user.equipeId:
        raise HTTPException(status_code=403, detail="Líder só pode desativar membros do seu time")
    user.active = False
    db.add(user)
    db.commit()
    return {"detail": "Usuário desativado"}