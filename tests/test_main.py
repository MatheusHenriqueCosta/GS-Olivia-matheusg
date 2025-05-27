from app.main import soma

def test_soma():
    assert soma(2, 3) == 5

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Bem-vindo" in response.data