import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient, mock_db_session: AsyncMock):
    payload = {
        "email": "test@example.com",
        "name": "TestUser",
        "password": "StrongPassword1!"
    }
    
    mock_user = AsyncMock()
    mock_user.id = 123
    mock_user.email = payload["email"]
    mock_user.name = payload["name"]
    
    with patch("apps.users.crud.user_manager.get", new_callable=AsyncMock) as mock_get, \
         patch("apps.users.crud.user_manager.create", new_callable=AsyncMock) as mock_create:
        
        # Scenario: User does not exist
        mock_get.return_value = None
        mock_create.return_value = mock_user
        
        response = await client.post("/users/create", json=payload)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == payload["email"]
        
        # Verify get was called to check for existing user
        mock_get.assert_called_once()
        # Verify create was called
        mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient, mock_db_session: AsyncMock):
    payload = {
        "email": "existing@example.com",
        "name": "ExistingUser",
        "password": "StrongPassword1!"
    }
    
    # Mock existing user
    existing_user = AsyncMock()
    existing_user.email = payload["email"]
    
    with patch("apps.users.crud.user_manager.get", new_callable=AsyncMock) as mock_get, \
         patch("apps.users.crud.user_manager.create", new_callable=AsyncMock) as mock_create:
        
        # Scenario: User already exists
        mock_get.return_value = existing_user
        
        response = await client.post("/users/create", json=payload)
        
        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert data["detail"] == "Email already registered"
        
        # Verify get was called
        mock_get.assert_called_once()
        # Verify create was NOT called
        mock_create.assert_not_called()


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
