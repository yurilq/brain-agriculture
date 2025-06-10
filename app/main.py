from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import produtor, fazenda, safra, cultura, dashboard
from app.core.database import Base, engine
from fastapi.staticfiles import StaticFiles
import logging

# Criação das tabelas no banco (comentada porque usamos alembic)
# Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa o app
app = FastAPI(
    title="Brain Agriculture API",
    version="1.0.0",
    description="API para gerenciamento de produtores, fazendas, safras e culturas.",
)

# Monta a pasta static
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas
app.include_router(produtor.router, prefix="/produtores", tags=["Produtores"])
app.include_router(fazenda.router, prefix="/fazendas", tags=["Fazendas"])
app.include_router(safra.router, prefix="/safras", tags=["Safras"])
app.include_router(cultura.router, prefix="/culturas", tags=["Culturas"])
app.include_router(dashboard.router)

# Rota simples de saúde
@app.get("/")
def root():
    return {"status": "API online"}
