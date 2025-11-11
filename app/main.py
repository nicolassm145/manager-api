from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.v1 import auth, users, equipes

from app.models.user import User
from app.models.equipe import Equipe
from app.models.item import Item
from app.models.transacao import Transacao

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