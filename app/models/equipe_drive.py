from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class EquipeDriveIntegration(Base):
    __tablename__ = "equipe_drive_integracao"

    id = Column(Integer, primary_key=True, index=True)
    equipeId = Column(Integer, ForeignKey('equipes.id'), unique=True, nullable=False)
    driveFolderId = Column(String, nullable=False)

    accessToken = Column(String, nullable=False)
    refreshToken = Column(String, nullable=False)
    tokenExpireAt = Column(DateTime, nullable=True)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.utcnow)

    equipe = relationship("Equipe")