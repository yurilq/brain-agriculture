from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_criar_produtor_com_cpf_invalido():
    response = client.post("/produtores/produtores/", json={
        "nome": "João Teste",
        "documento": "12345678900",  # CPF inválido
        "tipo_documento": "cpf"
    })
    assert response.status_code == 422
    assert "CPF inválido" in response.text




def test_fazenda_area_invalida():
    response = client.post("/fazendas/fazendas/", json={
        "nome": "Fazenda Inválida",
        "cidade": "Goiânia",
        "estado": "GO",
        "area_total": 10,
        "area_agricultavel": 6,
        "area_vegetacao": 6,  # Soma = 12 > total = 10
        "produtor_id": 1
    })
    # Validação customizada do Pydantic gera erro 422
    assert response.status_code == 422  # corrigido de 400 para 422
