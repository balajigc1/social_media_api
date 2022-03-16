import pytest
from fastapi.testclient import TestClient
from app import schemas
from app.main import app

client = TestClient(app)

def test_get_all_posts():
    result = client.get("/posts")
    assert result.status_code == 200

def test_post_does_not_exist():
    result = client.get("/posts/9999")
    assert result.status_code == 404

# def test_create_post():
#     result = client.post("/posts")
#     assert result.status_code == 201

# def test_delete_post():
#     result = client.delete("/posts/{test_posts[0].id}")
#     assert result.status_code == 204