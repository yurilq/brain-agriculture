from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.produtor import Produtor
from app.schemas.produtor import ProdutorCreate, ProdutorResponse
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/produtores",
    tags=["Produtores"]
)

@router.post("/", response_model=ProdutorResponse)
def criar_produtor(produtor: ProdutorCreate, db: Session = Depends(get_db)):
    logger.info("Criando produtor: %s", produtor)
    existente = db.query(Produtor).filter(Produtor.documento == produtor.documento).first()
    if existente:
        logger.warning("Documento já cadastrado: %s", produtor.documento)
        raise HTTPException(status_code=400, detail="Documento já cadastrado")
    novo = Produtor(**produtor.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    logger.info("Produtor criado com ID: %s", novo.id)
    return novo

@router.get("/", response_model=List[ProdutorResponse])
def listar_produtores(db: Session = Depends(get_db)):
    logger.info("Listando todos os produtores")
    return db.query(Produtor).all()

@router.get("/{id}", response_model=ProdutorResponse)
def buscar_produtor(id: int, db: Session = Depends(get_db)):
    logger.info("Buscando produtor ID: %s", id)
    produtor = db.query(Produtor).filter(Produtor.id == id).first()
    if not produtor:
        logger.warning("Produtor ID %s não encontrado", id)
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return produtor

@router.put("/{id}", response_model=ProdutorResponse)
def atualizar_produtor(id: int, dados: ProdutorCreate, db: Session = Depends(get_db)):
    logger.info("Atualizando produtor ID: %s com dados: %s", id, dados)
    produtor = db.query(Produtor).filter(Produtor.id == id).first()
    if not produtor:
        logger.warning("Produtor ID %s não encontrado para atualização", id)
        raise HTTPException(status_code=404, detail="Produtor não encontrado")

    if db.query(Produtor).filter(Produtor.documento == dados.documento, Produtor.id != id).first():
        logger.warning("Documento %s já utilizado por outro produtor", dados.documento)
        raise HTTPException(status_code=400, detail="Documento já utilizado por outro produtor")

    produtor.nome = dados.nome
    produtor.documento = dados.documento
    produtor.tipo_documento = dados.tipo_documento
    db.commit()
    db.refresh(produtor)
    logger.info("Produtor ID %s atualizado com sucesso", id)
    return produtor

@router.delete("/{id}", status_code=204)
def deletar_produtor(id: int, db: Session = Depends(get_db)):
    logger.info("Deletando produtor ID: %s", id)
    produtor = db.query(Produtor).filter(Produtor.id == id).first()
    if not produtor:
        logger.warning("Produtor ID %s não encontrado para exclusão", id)
        raise HTTPException(status_code=404, detail="Produtor não encontrado")

    db.delete(produtor)
    db.commit()
    logger.info("Produtor ID %s deletado com sucesso", id)
    return None
