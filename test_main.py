import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, engine
import models

# Crie um cliente de teste para a API
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

# Teste para o endpoint raiz
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo ao FastAPI!"}

# Teste para criar uma empresa
def test_create_empresa():
    empresa_data = {
        "nome": "Empresa Teste",
        "cnpj": "12345678901234",
        "endereco": "Rua Teste, 123",
        "email": "contato@empresateste.com",
        "telefone": "11987654321"
    }
    response = client.post("/empresas/", json=empresa_data)
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Teste"
    assert response.json()["cnpj"] == "12345678901234"

# Teste para consultar uma empresa por ID
def test_read_empresa():
    # Primeiro, crie uma empresa para testar a consulta
    empresa_data = {
        "nome": "Empresa Teste",
        "cnpj": "12345678901234",
        "endereco": "Rua Teste, 123",
        "email": "contato@empresateste.com",
        "telefone": "11987654321"
    }
    create_response = client.post("/empresas/", json=empresa_data)
    empresa_id = create_response.json()["id"]

    # Agora, consulte a empresa criada
    response = client.get(f"/empresas/{empresa_id}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Teste"
    assert response.json()["cnpj"] == "12345678901234"

# Teste para consultar uma empresa que não existe
def test_read_empresa_not_found():
    response = client.get("/empresas/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Empresa não encontrada"

def test_create_obrigacao():
    obrigacao_data = {
        "nome": "Obrigação Teste",
        "periodicidade": "mensal",
        "empresa_id": 1
    }
    response = client.post("/obrigacoes/", json=obrigacao_data)
    assert response.status_code == 200
    assert response.json()["nome"] == "Obrigação Teste"
    assert response.json()["periodicidade"] == "mensal"

def test_read_obrigacao():
    response = client.get("/obrigacoes/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Obrigação Teste"
    assert response.json()["periodicidade"] == "mensal"

def test_update_obrigacao():
    obrigacao_data = {
        "nome": "Obrigação Atualizada",
        "periodicidade": "trimestral",
        "empresa_id": 1
    }
    response = client.put("/obrigacoes/1", json=obrigacao_data)
    assert response.status_code == 200
    assert response.json()["nome"] == "Obrigação Atualizada"
    assert response.json()["periodicidade"] == "trimestral"

def test_delete_obrigacao():
    response = client.delete("/obrigacoes/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Obrigação excluída com sucesso"