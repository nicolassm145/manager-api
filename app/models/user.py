from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nomeCompleto = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    curso = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    tipoAcesso = Column(String, nullable=False)
    cargoEquipe = Column(String, nullable=True)
    equipeId = Column(Integer, ForeignKey("equipes.id"))
    dataInicio = Column(Date, nullable=False)
    ativo = Column(Boolean, nullable=False)

    equipe = relationship("Equipe", back_populates="membros")
    transacoes = relationship("Transacao", back_populates="user")