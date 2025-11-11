from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.equipe import Equipe
from app.schemas.equipe import EquipeCreate, EquipeUpdate, EquipeOut
from app.schemas.user import UserOut
from app.services.equipe_service import create_equipe, list_equipes, get_equipe_by_id, update_equipe, delete_equipe
from app.api.deps import getCurrentUser, requireTipoAcesso
from app.api.deps import getCurrentUser, requireTipoAcesso, User

router = APIRouter(prefix="/api/v1/equipes", tags=["Equipes"])


# Criar uma nova equipe - Administrador
@router.post("/criar", response_model=EquipeOut, status_code=status.HTTP_201_CREATED)
def create_equipe_endpoint(
    equipe_in: EquipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(requireTipoAcesso("Administrador"))
):
    try:
        equipe = create_equipe(db, nome=equipe_in.nome, descricao=equipe_in.descricao)
        return equipe
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Listar todas as equipes
# # Listar equipes (admin e líderes)
@router.get("/listAll", response_model=list[EquipeOut])
def list_equipes_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(requireTipoAcesso("Administrador", "Líder"))
):
    return list_equipes(db)

# Listar equipe por ID
@router.get("/listar/{equipe_id}", response_model=EquipeOut)
def get_equipe_endpoint(
    equipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(getCurrentUser)
):
    equipe = get_equipe_by_id(db, equipe_id)
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    if current_user.tipoAcesso.lower() != "administrador" and current_user.equipeId != equipe_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return equipe

# Atualizar equipe - Administrador e Líder
@router.put("/atualizar/{equipe_id}", response_model=EquipeOut)
def update_equipe_endpoint(
    equipe_id: int,
    equipe_in: EquipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(getCurrentUser)
):
    equipe = get_equipe_by_id(db, equipe_id)
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    if current_user.tipoAcesso.lower() not in ["administrador", "líder"]:
        raise HTTPException(status_code=403, detail="Permissão negada")
    if current_user.tipoAcesso.lower() == "líder" and current_user.equipeId != equipe_id:
        raise HTTPException(status_code=403, detail="Líder só pode editar sua própria equipe")

    equipe = update_equipe(db, equipe_id, equipe_in.nome, equipe_in.descricao)
    return equipe

# Deletar equipe - Administrador
@router.delete("/deletar/{equipe_id}", status_code=status.HTTP_200_OK)
def delete_equipe_endpoint(
    equipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(requireTipoAcesso("Administrador"))
):
    ok = delete_equipe(db, equipe_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    return {"detail": "Equipe deletada com sucesso"}

# Listar membros da equipe
@router.get("/{equipe_id}/membros", response_model=list[UserOut])
def listar_membros_equipe(
    equipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(getCurrentUser)
):
    equipe = db.query(Equipe).filter(Equipe.id == equipe_id).first()
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")

    if current_user.tipoAcesso.lower() != "administrador" and current_user.equipeId != equipe_id:
        raise HTTPException(status_code=403, detail="Acesso negado a membros de outras equipes")

    return equipe.membros
