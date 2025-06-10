from pydantic import BaseModel, Field, model_validator, ConfigDict

class FazendaBase(BaseModel):
    nome: str
    cidade: str
    estado: str = Field(..., min_length=2, max_length=2)
    area_total: float
    area_agricultavel: float
    area_vegetacao: float
    produtor_id: int

    @model_validator(mode="after")
    def validar_areas(self):
        if self.area_agricultavel + self.area_vegetacao > self.area_total:
            raise ValueError("Área agricultável + vegetação não pode ultrapassar a área total.")
        return self

class FazendaCreate(FazendaBase):
    pass

class FazendaResponse(FazendaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
