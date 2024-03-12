# a special file that pytest uses to define fixtures 
# any fixtures defined in this file are available throughout the package (even sub-packages)
# package specific

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test'

# engine responsible for establish connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # get a session do the db
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user
    

@pytest.fixture
def test_user_2(client):
    user_data = {"email": "hello12345@gmail.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user
    
@pytest.fixture()
def access_token(test_user):
    id = test_user["id"]
    return create_access_token({"user_id": id})

@pytest.fixture()
def authorized_client(client, access_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
        }
    
    return client

@pytest.fixture()
def test_posts(test_user, test_user_2, session):
    posts_data = [{"title": "1st title", "content": "1st content", "owner_id": test_user["id"]},
                  {"title": "2nd title", "content": "2nd content", "owner_id": test_user["id"]},
                  {"title": "3rd title", "content": "3rd content", "owner_id": test_user["id"]},
                   {"title": "4th title", "content": "4th content", "owner_id": test_user_2["id"]}]
    
    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts