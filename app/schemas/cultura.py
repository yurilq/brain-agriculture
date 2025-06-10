from pydantic import BaseModel, Field
from pydantic import ConfigDict

class CulturaBase(BaseModel):
    nome: str = Field(..., example="Milho")

class CulturaCreate(CulturaBase):
    pass

class CulturaUpdate(CulturaBase):  # ✅ necessário para PUT funcionar
    pass

class CulturaResponse(CulturaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
