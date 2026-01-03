import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient, mock_db_session: AsyncMock):
    payload = {
        "email": "test@example.com",
        "name": "TestUser",
        "password": "StrongPassword1!"
    }
    
    # Use `unittest.mock.patch` to mock the user_manager.create_user method
    from unittest.mock import patch
    
    # Create a fake user object to return
    mock_user = AsyncMock()
    mock_user.id = 123
    mock_user.email = payload["email"]
    mock_user.name = payload["name"]
    # Pydantic models expect dict access or attribute access depending on usage.
    # The router returns `RegisteredUserSchema`, which is created from the result of `create_user`.
    # `RegisteredUserSchema` will try to read attributes from the returned object.
    
    with patch("apps.users.router.user_manager.create_user", return_value=mock_user) as mock_create:
        response = await client.post("/users/create", json=payload)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == payload["email"]
        assert data["name"] == payload["name"]
        assert data["id"] == 123
        assert "password" not in data
        
        # Verify that the manager was called
        mock_create.assert_called_once()


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
