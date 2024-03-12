import pytest 
from app import models

@pytest.fixture 
def test_vote(test_user, test_posts, session):
    vote = {"post_id": test_posts[-1].id, "user_id": test_user["id"]}
    new_vote = models.Vote(**vote)
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)
    return new_vote


def test_vote_on_post(authorized_client, test_posts):
    data = {"post_id": test_posts[-1].id, "dir": 1}
    response = authorized_client.post("/vote", json=data)
    assert response.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    data = {"post_id": test_posts[-1].id, "dir": 1}
    response = authorized_client.post("/vote", json=data)
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    data = {"post_id": test_posts[-1].id, "dir": 0}
    response = authorized_client.post("/vote", json=data)
    assert response.status_code == 201

def test_delete_vote_nonexist(authorized_client, test_posts):
    data = {"post_id": test_posts[-1].id, "dir": 0}
    response = authorized_client.post("/vote", json=data)
    assert response.status_code == 404

def test_vote_post_non_exist(authorized_client, test_posts):
    data = {"post_id": -1, "dir": 0}
    response = authorized_client.post("/vote", json=data)
    assert response.status_code == 404

def test_unathorized_vote_on_post(client, test_posts):
    data = {"post_id": test_posts[-1].id, "dir": 1}
    response = client.post("/vote", json=data)
    assert response.status_code == 401
