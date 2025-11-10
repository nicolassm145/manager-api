from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.utils.security import hash_password

def create_user(db: Session, *, user_in):
    new_user = User(
        nomeCompleto=user_in.nomeCompleto,
        matricula=user_in.matricula,
        email=user_in.email,
        curso=user_in.curso,
        hashed_password=hash_password(user_in.password),
        tipoAcesso=user_in.tipoAcesso,
        cargoEquipe=user_in.cargoEquipe,
        equipeId=user_in.equipeId,
        dataInicio=user_in.dataInicio,
        ativo=user_in.ativo
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise e
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.ativo == True).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()