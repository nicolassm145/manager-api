from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.security import decodeToken
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decodeToken(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user_id = payload.get("id") or payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sem id")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.ativo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário inválido ou inativo")
    return user

def requireTipoAcesso(*tiposPermitidos: str):
    def tipoChecker(current_user: User = Depends(getCurrentUser)):
        if current_user.tipoAcesso not in tiposPermitidos:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado para este recurso")
        return current_user
    return tipoChecker

def checkUserAccess(current_user, target_user):
    # Admin pode tudo
    if current_user.tipoAcesso == "Administrador":
        return True

    # Líder e Membro só podem ver usuários da mesma equipe
    if current_user.tipoAcesso in ["Líder", "Membro"]:
        if current_user.equipeId == target_user.equipeId:
            return True
        else:
            raise HTTPException(status_code=403, detail="Acesso negado a membros de outra equipe")

    # Outros papéis: negar
    raise HTTPException(status_code=403, detail="Permissão negada")
