from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.equipe import Equipe
from datetime import date

def create_equipe(db: Session, nome: str, descricao: str, criado_em: date = None):
    equipe = Equipe(
        nome=nome, 
        descricao=descricao, 
        criadoEm=criado_em if criado_em else date.today()
    )
    db.add(equipe)
    try:
        db.commit()
        db.refresh(equipe)
    except IntegrityError:
        db.rollback()
        raise ValueError("Equipe com esse nome já existe.")
    return equipe

def get_equipe_by_id(db: Session, equipe_id: int):
    return db.query(Equipe).filter(Equipe.id == equipe_id).first()

def list_equipes(db: Session):
    return db.query(Equipe).all()

def update_equipe(db: Session, equipe_id: int, nome: str = None, descricao: str = None):
    equipe = get_equipe_by_id(db, equipe_id)
    if not equipe:
        return None
    if nome:
        equipe.nome = nome
    if descricao:
        equipe.descricao = descricao
    db.add(equipe)
    db.commit()
    db.refresh(equipe)
    return equipe

def delete_equipe(db: Session, equipe_id: int):
    equipe = get_equipe_by_id(db, equipe_id)
    if equipe:
        db.delete(equipe)
        db.commit()
        return True
    return False

