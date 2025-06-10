from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.fazenda import Fazenda
from app.models.produtor import Produtor
from app.schemas.fazenda import FazendaCreate, FazendaResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/fazendas",
    tags=["Fazendas"]
)

@router.post("/", response_model=FazendaResponse)
def criar_fazenda(fazenda: FazendaCreate, db: Session = Depends(get_db)):
    logger.info(f"Solicitação para criar fazenda: {fazenda}")
    produtor = db.query(Produtor).filter(Produtor.id == fazenda.produtor_id).first()
    if not produtor:
        logger.warning(f"Produtor ID {fazenda.produtor_id} não encontrado")
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    nova = Fazenda(**fazenda.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    logger.info(f"Fazenda criada com sucesso: {nova}")
    return nova

@router.get("/", response_model=List[FazendaResponse])
def listar_fazendas(db: Session = Depends(get_db)):
    logger.info("Listando todas as fazendas")
    return db.query(Fazenda).all()

@router.get("/{id}", response_model=FazendaResponse)
def buscar_fazenda(id: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando fazenda ID {id}")
    fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
    if not fazenda:
        logger.warning(f"Fazenda não encontrada: ID {id}")
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")
    return fazenda

@router.put("/{id}", response_model=FazendaResponse)
def atualizar_fazenda(id: int, dados: FazendaCreate, db: Session = Depends(get_db)):
    logger.info(f"Atualizando fazenda ID {id} com dados: {dados}")
    fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
    if not fazenda:
        logger.warning(f"Fazenda não encontrada para atualização: ID {id}")
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")

    fazenda.nome = dados.nome
    fazenda.area_total = dados.area_total
    fazenda.area_agricultavel = dados.area_agricultavel
    fazenda.area_vegetacao = dados.area_vegetacao
    fazenda.cidade = dados.cidade
    fazenda.estado = dados.estado
    fazenda.produtor_id = dados.produtor_id

    db.commit()
    db.refresh(fazenda)
    logger.info(f"Fazenda atualizada com sucesso: ID {id}")
    return fazenda

@router.delete("/{id}", status_code=204)
def deletar_fazenda(id: int, db: Session = Depends(get_db)):
    logger.info(f"Tentando deletar fazenda ID {id}")
    fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
    if not fazenda:
        logger.warning(f"Fazenda não encontrada para exclusão: ID {id}")
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")

    db.delete(fazenda)
    db.commit()
    logger.info(f"Fazenda deletada com sucesso: ID {id}")
    return None
