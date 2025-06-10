from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Safra(Base):
    __tablename__ = "safras"

    id = Column(Integer, primary_key=True, index=True)
    ano_inicio = Column(Date, nullable=False)
    ano_fim = Column(Date, nullable=False)

    fazenda_id = Column(Integer, ForeignKey("fazendas.id"), nullable=False)
    fazenda = relationship("Fazenda", back_populates="safras")

    cultura_id = Column(Integer, ForeignKey("culturas.id"))
    cultura = relationship("Cultura", back_populates="safras")
