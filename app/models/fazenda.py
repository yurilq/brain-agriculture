from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Fazenda(Base):
    __tablename__ = "fazendas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String(2), nullable=False)
    area_total = Column(Float, nullable=False)
    area_agricultavel = Column(Float, nullable=False)
    area_vegetacao = Column(Float, nullable=False)
    
    produtor_id = Column(Integer, ForeignKey("produtores.id"), nullable=False)
    produtor = relationship("Produtor", back_populates="fazendas")

    safras = relationship("Safra", back_populates="fazenda", cascade="all, delete-orphan")
