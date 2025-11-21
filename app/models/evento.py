from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    equipeId = Column(Integer, ForeignKey('equipes.id'), nullable=False)

    googleEventId = Column(String, nullable=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    startDatetime = Column(DateTime, nullable=False)
    endDatetime = Column(DateTime, nullable=False)

    createdAt = Column(DateTime, default=datetime.utcnow)

    equipe = relationship("Equipe", back_populates="eventos")
    participantes = relationship("EventoParticipante", cascade="all,delete")
    tarefas = relationship("EventoTarefa", cascade="all,delete")


class EventoParticipante(Base):
    __tablename__ = "evento_participantes"

    id = Column(Integer, primary_key=True, index=True)
    eventoId = Column(Integer, ForeignKey('eventos.id'), nullable=False)
    membroId = Column(Integer, ForeignKey('users.id'), nullable=False)

    status = Column(String, nullable=False, default="pendente")  # pendente, confirmado, recusado

    observacao = Column(Text, nullable=True)
    updatedAt = Column(DateTime, onupdate=datetime.utcnow)


class EventoTarefa(Base):
    __tablename__ = "evento_tarefas"

    id = Column(Integer, primary_key=True, index=True)
    eventoId = Column(Integer, ForeignKey('eventos.id'), nullable=False)
    membroId = Column(Integer, ForeignKey('users.id'), nullable=False)

    descricao = Column(Text, nullable=False)
    concluido = Column(Boolean, default=False)

    updatedAt = Column(DateTime, onupdate=datetime.utcnow)