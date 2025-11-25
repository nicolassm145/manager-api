from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Equipe(Base):
    __tablename__ = "equipes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    descricao = Column(String, nullable=True)
    criadoEm = Column(Date, nullable=False)

    membros = relationship("User", back_populates="equipe")
    itens = relationship("Item", back_populates="equipe")
    transacoes = relationship("Transacao", back_populates="equipe")
    eventos = relationship("Evento", back_populates="equipe", cascade="all, delete")