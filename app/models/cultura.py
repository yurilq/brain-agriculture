from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cultura(Base):
    __tablename__ = "culturas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    safras = relationship("Safra", back_populates="cultura")
