import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.safra import Safra
from app.schemas.safra import SafraCreate, SafraUpdate, SafraResponse

from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/safras", tags=["Safras"])

@router.post("/", response_model=SafraResponse)
def criar_safra(safra: SafraCreate, db: Session = Depends(get_db)):
    logger.info(f"Criando safra: {safra}")
    nova_safra = Safra(**safra.dict())
    db.add(nova_safra)
    db.commit()
    db.refresh(nova_safra)
    return nova_safra

@router.get("/", response_model=List[SafraResponse])
def listar_safras(db: Session = Depends(get_db)):
    logger.info("Listando todas as safras")
    return db.query(Safra).all()

@router.get("/{id}", response_model=SafraResponse)
def buscar_safra(id: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando safra ID: {id}")
    safra = db.query(Safra).filter(Safra.id == id).first()
    if not safra:
        logger.warning(f"Safra {id} não encontrada")
        raise HTTPException(status_code=404, detail="Safra não encontrada")
    return safra

@router.put("/{id}", response_model=SafraResponse)
def atualizar_safra(id: int, dados: SafraUpdate, db: Session = Depends(get_db)):
    logger.info(f"Atualizando safra ID: {id}")
    safra = db.query(Safra).filter(Safra.id == id).first()
    if not safra:
        logger.warning(f"Safra {id} não encontrada para atualização")
        raise HTTPException(status_code=404, detail="Safra não encontrada")
    
    for campo, valor in dados.dict(exclude_unset=True).items():
        setattr(safra, campo, valor)
    
    db.commit()
    db.refresh(safra)
    return safra

@router.delete("/{id}", status_code=204)
def deletar_safra(id: int, db: Session = Depends(get_db)):
    logger.info(f"Deletando safra ID: {id}")
    safra = db.query(Safra).filter(Safra.id == id).first()
    if not safra:
        logger.warning(f"Safra {id} não encontrada para deleção")
        raise HTTPException(status_code=404, detail="Safra não encontrada")

    db.delete(safra)
    db.commit()
