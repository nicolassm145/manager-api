from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EquipeDriveCreate(BaseModel):
    equipeId: int

class EquipeDriveOut(BaseModel):
    id: int
    equipeId: int
    driveFolderId: str
    createdAt: Optional[datetime]

    class Config:
        from_attributes = True

