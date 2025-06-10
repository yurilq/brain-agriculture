from datetime import date
from pydantic import BaseModel, Field
from typing import Optional
from pydantic import ConfigDict

class SafraBase(BaseModel):
    ano_inicio: date = Field(..., json_schema_extra={"example": "2024-06-01"})
    ano_fim: date = Field(..., json_schema_extra={"example": "2025-05-01"})
    fazenda_id: int
    cultura_id: Optional[int]

class SafraCreate(SafraBase):
    pass

class SafraUpdate(SafraBase):  # ✅ necessário para evitar erro de import
    pass

class SafraResponse(SafraBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
