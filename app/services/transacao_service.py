from sqlalchemy.orm import Session

from app.models.transacao import Transacao

def create_transacao(db, data, user):
    transacao = Transacao(
        descricao=data.descricao,
        valor=data.valor,
        data=data.data,
        tipo=data.tipo,
        categoria=data.categoria,
        equipeId=data.equipeId,
        criadoPor=user.id
    )
    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao

def update_transacao(db, transacao, data):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(transacao, field, value)

    db.commit()
    db.refresh(transacao)
    return transacao

def delete_transacao(db, transacao):
    db.delete(transacao)
    db.commit()