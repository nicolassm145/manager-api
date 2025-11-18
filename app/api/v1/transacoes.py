from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date   

from app.core.database import get_db
from app.api.deps import getCurrentUser, requireTipoAcesso

from app.schemas.transacao import (
    TransacaoCreate,
    TransacaoOut,
    TransacaoUpdate
)

from app.models.transacao import Transacao
from app.services.transacao_service import (
    create_transacao,
    update_transacao,
    delete_transacao
)

router = APIRouter(prefix="/api/v1/transacoes", tags=["Transações"])

# Rota para criar uma nova transação
@router.post("/criar", response_model=TransacaoOut)
def create_transacao_endpoint(data: TransacaoCreate, db=Depends(get_db), current_user=Depends(getCurrentUser)):

    if current_user.tipoAcesso == "Membro":
        raise HTTPException(403, "Membro não pode criar transações")

    if current_user.tipoAcesso == "Líder" and current_user.equipeId != data.equipeId:
        raise HTTPException(403, "Líder só pode criar para sua equipe")

    return create_transacao(db, data, current_user)

#Rota para listar transações com filtros
@router.get("/listar", response_model=list[TransacaoOut])
def list_transacoes(
    categoria: str = None,
    tipo: str = None,
    dataInicio: date = None,
    dataFim: date = None,
    db=Depends(get_db),
    current_user=Depends(getCurrentUser)
):

    query = db.query(Transacao)

    if current_user.tipoAcesso != "Administrador":
        query = query.filter(Transacao.equipeId == current_user.equipeId)

    if categoria:
        query = query.filter(Transacao.categoria.ilike(f"%{categoria}%"))

    if tipo:
        query = query.filter(Transacao.tipo == tipo)

    if dataInicio and dataFim:
        query = query.filter(Transacao.data.between(dataInicio, dataFim))

    return query.all()

# Rota para atualizar uma transação
@router.put("/atualizar/{id}", response_model=TransacaoOut)
def update_transacao_endpoint(id: int, data: TransacaoUpdate, db=Depends(get_db), current_user=Depends(getCurrentUser)):

    transacao = db.query(Transacao).filter(Transacao.id == id).first()
    if not transacao:
        raise HTTPException(404, "Transação não encontrada")

    if current_user.tipoAcesso == "Membro":
        raise HTTPException(403, "Membro não pode alterar transações")

    if current_user.tipoAcesso == "Líder" and current_user.equipeId != transacao.equipeId:
        raise HTTPException(403, "Líder só pode alterar transações da própria equipe")

    return update_transacao(db, transacao, data)

# Rota para deletar uma transação
@router.delete("/deletar/{id}", status_code=200)
def delete_transacao_endpoint(id: int, db=Depends(get_db), current_user=Depends(getCurrentUser)):
    transacao = db.query(Transacao).filter(Transacao.id == id).first()
    if not transacao:
        raise HTTPException(404, "Transação não encontrada")

    if current_user.tipoAcesso == "Administrador":
        pass  # Admin pode deletar qualquer transação
    elif current_user.tipoAcesso == "Líder":
        if current_user.equipeId != transacao.equipeId:
            raise HTTPException(403, "Líder só pode deletar transações da própria equipe")
    else:
        raise HTTPException(403, "Somente administradores ou líderes podem deletar transações")

    delete_transacao(db, transacao)
    return {"detail": "Transação removida com sucesso"}