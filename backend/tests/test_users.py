import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient):
    payload = {
        "email": "test@example.com",
        "name": "TestUser",
        "password": "StrongPassword1!"
    }
    response = await client.post("/users/create", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert "id" in data
    assert "password" not in data  # Ensure password is not returned

@pytest.mark.asyncio
async def test_create_user_invalid_password(client: AsyncClient):
    payload = {
        "email": "test@example.com",
        "name": "TestUser",
        "password": "weak"
    }
    response = await client.post("/users/create", json=payload)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    data = response.json()
    assert "detail" in data
    # Check that the error message relates to password validation
    assert any("password" in str(err["loc"]) for err in data["detail"])

@pytest.mark.asyncio
async def test_create_user_invalid_email(client: AsyncClient):
    payload = {
        "email": "invalid-email",
        "name": "TestUser",
        "password": "StrongPassword1!"
    }
    response = await client.post("/users/create", json=payload)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
