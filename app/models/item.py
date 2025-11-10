from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Item(Base):
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sku = Column(String, unique=True)
    categoria = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    localizacao = Column(String, nullable=False)
    equipeId = Column(Integer, ForeignKey("equipes.id"))

    equipe = relationship("Equipe", back_populates="itens")