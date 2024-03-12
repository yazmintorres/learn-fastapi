from app import schemas
import pytest

# GET REQUESTS

def test_get_all_posts(authorized_client, test_posts ):
    response = authorized_client.get("/posts")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, response.json())
    posts = list(posts_map)
    assert len(posts) == len(test_posts)
    assert response.status_code == 200

def test_unathorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts")
    assert response.status_code == 401

def test_unathorized_user_get_one_post(client, test_posts):
    id = test_posts[0].id
    response = client.get(f"/posts/{id}")
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/posts/-1")
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    id = test_posts[0].id
    response = authorized_client.get(f"/posts/{id}")
    post = schemas.PostOut(**response.json())
    assert post.post.id == id
    assert response.status_code == 200

# POST REQUESTS

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True), 
    ("favorite pizze", "I love pepperonie", False), 
    ("tallest skyscraper", "Wahoo", True)
    ] )
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts", json={"title": title, "content": content, "published": published})
    new_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert test_user["id"] == new_post.owner_id

@pytest.mark.parametrize("title, content", [
    ("awesome new title", "awesome new content"), 
    ("favorite pizze", "I love pepperonie"), 
    ("tallest skyscraper", "Wahoo")
    ] )
def test_create_post_default_published_true(authorized_client, test_user, title, content):
    response = authorized_client.post("/posts", json={"title": title, "content": content})
    new_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert new_post.published == True

def test_unathorized_user_create_post(client, test_posts):
    response = client.post("/posts", json={"title": "title", "content": "content"})
    assert response.status_code == 401

# DELETE REQUESTS

def test_unauthorized_delete_post(client, test_posts):
    id = test_posts[0].id
    response = client.delete(f"/posts/{id}")
    assert response.status_code == 401
    
def test_delete_post_success(authorized_client, test_posts):
    id = test_posts[0].id
    response = authorized_client.delete(f"/posts/{id}")
    posts = authorized_client.get("/posts")
    assert len(posts.json()) == len(test_posts) - 1
    assert response.status_code == 204
    
def test_delete_post_nonexist(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/-1")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    user_2_post_id = test_posts[-1].id
    response = authorized_client.delete(f"/posts/{user_2_post_id}")
    assert response.status_code == 403


# PUT REQUESTS

def test_update_post(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_post_nonexist(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    response = authorized_client.put(f"/posts/{-1}", json=data)
    assert response.status_code == 404

def test_update_other_user_post(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    user_2_post_id = test_posts[-1].id
    response = authorized_client.put(f"/posts/{user_2_post_id}", json=data)
    assert response.status_code == 403

def test_unauthorized_update_post(client, test_posts):
    id = test_posts[0].id
    response = client.put(f"/posts/{id}")
    assert response.status_code == 401

