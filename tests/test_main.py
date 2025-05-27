import pytest
from app.main import app  # Importe sua aplicação Flask

@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):  # Corrigido o nome do teste e sintaxe
    """Testa a página inicial"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Bem-vindo" in response.data  # Adapte ao conteúdo da sua página

def test_health_endpoint(client):
    """Testa o endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    assert b"status" in response.data