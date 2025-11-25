from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.v1 import auth, transacoes, users, equipes, inventario, dashboard_financeiro, google_drive, google_calendar, eventos

from app.models.item import Item
from app.models.user import User
from app.models.equipe import Equipe
from app.models.item import Item
from app.models.transacao import Transacao
from app.models.equipe_drive import EquipeDriveIntegration
from app.models.evento import Evento, EventoParticipante, EventoTarefa

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="League Manager API",
    description="API para gerenciamento de equipes, membros, inventário e finanças",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

@app.get("/")
def root():
    return {"message": "🚀 League Manager API rodando com sucesso!"}

@app.get("/health/db")
def test_db_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                return {"status": "Banco conectado com sucesso!"}
    except Exception as e:
        return {"status": "Falha ao conectar com o banco", "erro": str(e)}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(equipes.router)
app.include_router(transacoes.router)
app.include_router(inventario.router)
app.include_router(dashboard_financeiro.router)
app.include_router(google_drive.router)
app.include_router(google_calendar.router)
app.include_router(eventos.router)
