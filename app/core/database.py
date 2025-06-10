from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

# URL de conexão com fallback para uso local/docke
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/brain")

# Criação do engine e sessão
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()

# Função de dependência para obter uma sessão do banco
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
