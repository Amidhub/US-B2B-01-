import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from src.main import app
from src.dependencies.auth import get_current_seller_id

client = TestClient(app)

def test_create_product_returns_201_with_created_status():
    app.dependency_overrides[get_current_seller_id] = lambda: uuid4()
    
    response = client.post("/api/v1/products", json={
        "title": "iPhone 15 Pro Max",
        "description": "Флагманский смартфон",
        "category_id": str(uuid4()),
        "images": [
            {"url": "/s3/front.jpg", "ordering": 0},
            {"url": "/s3/back.jpg", "ordering": 1}
        ],
        "characteristics": [
            {"name": "Бренд", "value": "Apple"}
        ]
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "CREATED"
    assert data["skus"] == []
    assert data["deleted"] == False
    assert data["blocked"] == False

def test_seller_id_taken_from_jwt():
    fixed_id = uuid4()
    app.dependency_overrides[get_current_seller_id] = lambda: fixed_id
    
    response = client.post("/api/v1/products", json={
        "title": "Test Product",
        "description": "Test Description",
        "category_id": str(uuid4()),
        "images": [{"url": "/s3/test.jpg", "ordering": 0}]
    })
    
    assert response.status_code == 201
    assert response.json()["seller_id"] == str(fixed_id)

def test_missing_images_returns_400():
    response = client.post("/api/v1/products", json={
        "title": "Test",
        "description": "Test",
        "category_id": str(uuid4())
    })
    
    assert response.status_code == 422

def test_missing_category_returns_400():
    response = client.post("/api/v1/products", json={
        "title": "Test",
        "description": "Test",
        "images": [{"url": "/s3/test.jpg", "ordering": 0}]
    })
    
    assert response.status_code == 422

def test_empty_title_returns_400():
    response = client.post("/api/v1/products", json={
        "title": "",
        "description": "Test",
        "category_id": str(uuid4()),
        "images": [{"url": "/s3/test.jpg", "ordering": 0}]
    })
    
    assert response.status_code == 422