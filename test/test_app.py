from fastapi.testclient import TestClient
import pytest
import sys
import os

# Adicionar o diretório raiz do projeto ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app


@pytest.fixture
def client():
    return TestClient(app)

email_token = ""
token       = ""

def test_register_user(client):
    user_data = {
        'name': 'Eduardo Soares',
        'email': 'test@example.com',
        'password': 'testpassword'
    }

    response = client.post('/api/v1/user/register', json=user_data)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        'name': 'Eduardo Soares',
        'email': 'test@example.com',
        'status': 1,
    }


def test_login(client):

    form_data = {
        'username': 'test@example.com',
        'password': 'testpassword'
    }

    response = client.post('/api/v1/user/login', data=form_data)

    assert response.status_code == 200
    payload = response.json()
    assert "access_token" in payload
    assert "token_type" in payload
    assert isinstance(payload["access_token"], str)
    assert payload["token_type"] == "Bearer"


def test_post_recover(client):

    user_data = {
        'email': 'test@example.com',
    }

    response = client.post('/api/v1/user/recoverpass', json=user_data)

    assert response.status_code == 200
    payload = response.json()
    email_token = payload["email_token"]
    assert "msg" in payload
    assert "email_token" in payload
    assert isinstance(payload["email_token"], str)


def test_get_recover(client):

    recovery_url = f"/api/v1/user/recoverpass/{email_token}"
    print(recovery_url)
    response = client.get(recovery_url)

    assert response.status_code == 401
    payload = response.json()
    assert "access_token" in payload
    assert "token_type" in payload
    assert isinstance(payload["access_token"], str)
    assert payload["token_type"] == "Bearer"
    

def test_get_user(client):

    form_data = {
        'username': 'test@example.com',
        'password': 'testpassword'
    }

    response_auth = client.post('/api/v1/user/login', data=form_data)
    assert response_auth.status_code == 200
    token = response_auth.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get('/api/v1/user/1', headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        'name': 'Eduardo Soares',
        'email': 'test@example.com',
        'status': 1,
    }