from pydantic import BaseModel, ConfigDict, model_validator
from typing import Literal
from validate_docbr import CPF, CNPJ

class ProdutorBase(BaseModel):
    nome: str
    documento: str
    tipo_documento: Literal["cpf", "cnpj"]

    @model_validator(mode="after")
    def validar_documento(self):
        if self.tipo_documento == "cpf" and not CPF().validate(self.documento):
            raise ValueError("CPF inválido")
        elif self.tipo_documento == "cnpj" and not CNPJ().validate(self.documento):
            raise ValueError("CNPJ inválido")
        return self

class ProdutorCreate(ProdutorBase):
    pass

class ProdutorResponse(ProdutorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
