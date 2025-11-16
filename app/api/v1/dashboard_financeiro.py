from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case, or_
from datetime import date, datetime
from typing import List

from app.core.database import get_db
from app.api.deps import getCurrentUser
from app.models.transacao import Transacao

router = APIRouter(prefix="/api/v1/transacoes/dashboard", tags=["Dashboard Financeiro"])

# Rota para obter resumo financeiro

@router.get("/resumo")
def resumo_financeiro(db: Session = Depends(get_db), current_user=Depends(getCurrentUser)):
    entrada_case = case(
        (
            func.lower(Transacao.tipo) == "entrada",
            Transacao.valor
        ),
        else_=0
    )
    saida_case = case(
        (
            or_(
                func.lower(Transacao.tipo) == "saida",
                func.lower(Transacao.tipo) == "saída"
            ),
            Transacao.valor
        ),
        else_=0
    )

    query = db.query(
        func.sum(entrada_case).label("total_entradas"),
        func.sum(saida_case).label("total_saidas")
    )

    if current_user.tipoAcesso.lower() != "administrador":
        query = query.filter(Transacao.equipeId == current_user.equipeId)

    resultado = query.first()

    total_entradas = float(resultado.total_entradas or 0)
    total_saidas = float(resultado.total_saidas or 0)

    return {
        "entradas": total_entradas,
        "saidas": total_saidas,
        "saldo": total_entradas - total_saidas
    }

# Rota para obter histórico mensal
@router.get("/mensal")
def historico_mensal(
    ano: int,
    db: Session = Depends(get_db),
    current_user = Depends(getCurrentUser)
):
    entrada_case = case(
        (
            func.lower(Transacao.tipo) == "entrada",
            Transacao.valor
        ),
        else_=0
    )
    saida_case = case(
        (
            or_(
                func.lower(Transacao.tipo) == "saida",
                func.lower(Transacao.tipo) == "saída"
            ),
            Transacao.valor
        ),
        else_=0
    )
    query = db.query(
        extract('month', Transacao.data).label("mes"),
        func.sum(entrada_case).label("entradas"),
        func.sum(saida_case).label("saidas")
    ).filter(extract('year', Transacao.data) == ano)

    if current_user.tipoAcesso != "Administrador":
        query = query.filter(Transacao.equipeId == current_user.equipeId)

    query = query.group_by(extract('month', Transacao.data)).order_by(extract('month', Transacao.data))

    resultado = query.all()

    mensal = {
        int(row.mes): {
            "entradas": float(row.entradas or 0),
            "saidas": float(row.saidas or 0)
        }
        for row in resultado
    }

    return mensal

# Rota para obter total por categoria
@router.get("/categorias")
def total_por_categoria(
    db: Session = Depends(get_db),
    current_user = Depends(getCurrentUser)
):
    query = db.query(
        Transacao.categoria,
        func.sum(Transacao.valor).label("total")
    )

    if current_user.tipoAcesso != "Administrador":
        query = query.filter(Transacao.equipeId == current_user.equipeId)

    query = query.group_by(Transacao.categoria)

    resultado = query.all()

    return {categoria: float(total) for categoria, total in resultado}

# Rota para obter últimas 10 transações
@router.get("/ultimas")
def ultimas_transacoes(
    db: Session = Depends(get_db),
    current_user = Depends(getCurrentUser)
):
    query = db.query(Transacao)

    if current_user.tipoAcesso != "Administrador":
        query = query.filter(Transacao.equipeId == current_user.equipeId)

    transacoes = query.order_by(Transacao.data.desc()).limit(10).all()

    return transacoes