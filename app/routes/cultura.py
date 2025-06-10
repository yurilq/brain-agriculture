import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.cultura import Cultura
from app.schemas.cultura import CulturaCreate, CulturaResponse, CulturaUpdate
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/culturas", tags=["Culturas"])

@router.post("/", response_model=CulturaResponse)
def criar_cultura(cultura: CulturaCreate, db: Session = Depends(get_db)):
    logger.info(f"Criando cultura: {cultura}")
    nova_cultura = Cultura(**cultura.dict())
    db.add(nova_cultura)
    db.commit()
    db.refresh(nova_cultura)
    return nova_cultura

@router.get("/", response_model=List[CulturaResponse])
def listar_culturas(db: Session = Depends(get_db)):
    logger.info("Listando todas as culturas")
    return db.query(Cultura).all()

@router.get("/{id}", response_model=CulturaResponse)
def buscar_cultura(id: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando cultura ID: {id}")
    cultura = db.query(Cultura).filter(Cultura.id == id).first()
    if not cultura:
        logger.warning(f"Cultura {id} não encontrada")
        raise HTTPException(status_code=404, detail="Cultura não encontrada")
    return cultura

@router.put("/{id}", response_model=CulturaResponse)
def atualizar_cultura(id: int, dados: CulturaUpdate, db: Session = Depends(get_db)):
    logger.info(f"Atualizando cultura ID: {id}")
    cultura = db.query(Cultura).filter(Cultura.id == id).first()
    if not cultura:
        logger.warning(f"Cultura {id} não encontrada para atualização")
        raise HTTPException(status_code=404, detail="Cultura não encontrada")
    
    for campo, valor in dados.dict(exclude_unset=True).items():
        setattr(cultura, campo, valor)
    
    db.commit()
    db.refresh(cultura)
    return cultura

@router.delete("/{id}", status_code=204)
def deletar_cultura(id: int, db: Session = Depends(get_db)):
    logger.info(f"Deletando cultura ID: {id}")
    cultura = db.query(Cultura).filter(Cultura.id == id).first()
    if not cultura:
        logger.warning(f"Cultura {id} não encontrada para deleção")
        raise HTTPException(status_code=404, detail="Cultura não encontrada")

    db.delete(cultura)
    db.commit()
