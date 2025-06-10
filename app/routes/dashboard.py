from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import Depends
from sqlalchemy import func
from app.models.fazenda import Fazenda
from app.models.cultura import Cultura
from app.models.safra import Safra
from fastapi.responses import FileResponse
import logging

router = APIRouter()

@router.get("/dashboard/resumo")
def dashboard_resumo(db: Session = Depends(get_db)):
    total_fazendas = db.query(Fazenda).count()
    total_hectares = db.query(func.sum(Fazenda.area_total)).scalar() or 0.0

    por_estado = (
        db.query(Fazenda.estado, func.count(Fazenda.id))
        .group_by(Fazenda.estado)
        .all()
    )
    por_cultura = (
        db.query(Cultura.nome, func.count(Safra.id))
        .join(Safra, Cultura.id == Safra.cultura_id)
        .group_by(Cultura.nome)
        .all()
    )

    uso_solo = db.query(
        func.sum(Fazenda.area_agricultavel), func.sum(Fazenda.area_vegetacao)
    ).first()

    resumo = {
        "total_fazendas": total_fazendas,
        "total_hectares": total_hectares,
        "por_estado": [{"estado": e, "total": t} for e, t in por_estado],
        "por_cultura": [{"cultura": c, "total": t} for c, t in por_cultura],
        "uso_solo": {
            "agricultavel": uso_solo[0] or 0.0,
            "vegetacao": uso_solo[1] or 0.0,
        },
    }

    logging.info("Dashboard resumo gerado com sucesso")
    return resumo

# ✅ NOVA ROTA HTML
@router.get("/dashboard/html")
def dashboard_html():
    return FileResponse("static/dashboard_grafico.html")
