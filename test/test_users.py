import pytest
from fastapi.testclient import TestClient
from app import schemas
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
 

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:balaji123@localhost:5432/fastapi_test'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally: 
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_root():
    result = client.get("/")
    assert result.json().get('Message') == 'Hello World'
    assert result.status_code == 200

# def test_create_user():
#     result = client.post("/users/", json={"email": "balaji1234@gmail.com", "password": "password123"})

#     new_user = schemas.UserResponse(**result.json())
#     assert new_user.email == "balaji1234@gmail.com"    
#     assert result.status_code == 201
