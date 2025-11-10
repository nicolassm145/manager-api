from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    equipeId = Column(Integer, ForeignKey("equipes.id"), nullable=False)
    criadoPor = Column(Integer, ForeignKey("users.id"), nullable=False)

    equipe = relationship("Equipe", back_populates="transacoes")
    user = relationship("User", back_populates="transacoes")