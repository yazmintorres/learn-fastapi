from app import schemas
from app.config import settings
from jose import jwt
import pytest

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

def test_create_user(client):
    response = client.post("/users", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "hello123@gmail.com"

def test_login_user(client, test_user):
    # first create a user, data for form data
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    
    # validate that we get back the response we expect
    login_response = schemas.Token(**response.json())

    # validate token
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms= [settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrong_email@gmail.com", "password_123", 404),
    ("hello123@gmail.com", "wrong_password", 401),
    ("wrong_email@gmail.com", "wrong_password", 404),
    (None, "password_123", 422),
    ("hello123@gmail.com", None, 422)
    ])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid credentials"




