from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.item import ItemCreate, ItemOut, ItemUpdate
from app.services.item_service import create_item, update_item, delete_item
from app.models.item import Item
from app.models.user import User
from app.api.deps import getCurrentUser

router = APIRouter(prefix="/api/v1/itens", tags=["Inventário"])

#Rota para criar um novo item no inventário
@router.post("/criar", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(item_in: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(getCurrentUser)):
    
    if current_user.tipoAcesso not in ["Administrador", "Líder", "Membro"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    if current_user.tipoAcesso == "Líder" and current_user.equipeId != item_in.equipeId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Líder só pode criar itens para sua própria equipe.")
    
    if current_user.tipoAcesso == "Membro" and current_user.equipeId != item_in.equipeId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Membro só pode criar itens para sua própria equipe.")
    
    try:
        return create_item(db, item_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Rota para listar todos os itens do inventário
@router.get("/listar", response_model=list[ItemOut])
def list_items(
    db: Session = Depends(get_db), 
    current_user: User = Depends(getCurrentUser), 
    nome: str = None, 
    categoria: str = None, 
    sku: str = None
):
    query = db.query(Item)

    if current_user.tipoAcesso != "Administrador":
        query = query.filter(Item.equipeId == current_user.equipeId)

    if nome:
        query = query.filter(Item.nome.ilike(f"%{nome}%"))
    if categoria:
        query = query.filter(Item.categoria.ilike(f"%{categoria}%"))
    if sku:
        query = query.filter(Item.sku.ilike(f"%{sku}%"))
    
    return query.all()

# Rota para buscar um item do inventário por ID
@router.get("/listar/{item_id}", response_model=ItemOut)
def get_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(getCurrentUser)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    if current_user.tipoAcesso.lower() != "administrador" and current_user.equipeId != item.equipeId:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return item

#Rota para atualizar um item do inventário
@router.put("/atualizar/{item_id}", response_model=ItemOut)
def update_item_endpoint(
    item_id: int, 
    item_in: ItemUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(getCurrentUser)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado.")
    
    if current_user.tipoAcesso == "Líder" and current_user.equipeId != item.equipeId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Líder só pode atualizar itens da sua própria equipe.")
    
    if current_user.tipoAcesso == "Membro" and current_user.equipeId != item.equipeId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Membro só pode atualizar itens da sua própria equipe.")
    
    return update_item(db, item, item_in)

#Rota para deletar um item do inventário
@router.delete("/deletar/{item_id}", status_code=status.HTTP_200_OK)
def delete_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(getCurrentUser)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado.")
    
    if current_user.tipoAcesso == "Líder" and current_user.equipeId != item.equipeId:
        raise HTTPException(403, "Líder só pode remover itens da própria equipe")
    
    if current_user.tipoAcesso == "Membro":
        raise HTTPException(403, "Membro não pode remover itens")
    
    
    delete_item(db, item)
    return {"detail": "Item removido com sucesso"}

