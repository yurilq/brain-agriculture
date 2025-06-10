from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Produtor(Base):
    __tablename__ = "produtores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    documento = Column(String(18), unique=True, nullable=False)
    tipo_documento = Column(String(4), nullable=False)  # <- ADICIONADO corretamente

    fazendas = relationship("Fazenda", back_populates="produtor", cascade="all, delete")
