import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from apps.users.models import User
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_force_logout_success(client: AsyncClient):
    # Mock user
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.use_token_since = None

    # Mock payload
    mock_payload = {
        "sub": "1",
        "email": "test@example.com",
        "iat": datetime.datetime.now(datetime.timezone.utc).timestamp(),
    }

    with (
        patch(
            "apps.auth.auth_handler.auth_handler.decode_token", new_callable=AsyncMock
        ) as mock_decode,
        patch(
            "apps.users.crud.user_manager.get", new_callable=AsyncMock
        ) as mock_get_user,
        patch(
            "apps.users.crud.user_manager.patch", new_callable=AsyncMock
        ) as mock_patch,
    ):
        mock_decode.return_value = mock_payload
        mock_get_user.return_value = mock_user

        # Call the endpoint
        headers = {"Authorization": "Bearer dummy_token"}
        response = await client.post("/auth/force-logout", headers=headers)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify patch was called
        mock_patch.assert_called_once()
        args, kwargs = mock_patch.call_args

        # instance_id is passed as a positional argument
        assert args[0] == mock_user.id

        # Verify that we are updating use_token_since
        assert "data_to_patch" in kwargs
        assert kwargs["data_to_patch"].use_token_since is not None


@pytest.mark.asyncio
async def test_access_token_expired_by_force_logout(client: AsyncClient):
    # Setup times
    now = datetime.datetime.now(datetime.timezone.utc)
    past = now - datetime.timedelta(minutes=10)

    # Mock user with use_token_since set to NOW (newer than token)
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.use_token_since = now

    # Mock payload with iat in the PAST
    mock_payload = {"sub": "1", "email": "test@example.com", "iat": past.timestamp()}

    with (
        patch(
            "apps.auth.auth_handler.auth_handler.decode_token", new_callable=AsyncMock
        ) as mock_decode,
        patch(
            "apps.users.crud.user_manager.get", new_callable=AsyncMock
        ) as mock_get_user,
    ):
        mock_decode.return_value = mock_payload
        mock_get_user.return_value = mock_user

        # Call a protected endpoint
        headers = {"Authorization": "Bearer old_token"}
        response = await client.post("/auth/force-logout", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Session expired. Please re-authenticate."


@pytest.mark.asyncio
async def test_refresh_token_expired_by_force_logout(client: AsyncClient):
    # Setup times
    now = datetime.datetime.now(datetime.timezone.utc)
    past = now - datetime.timedelta(minutes=10)

    # Mock user with use_token_since set to NOW
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.use_token_since = now

    # Mock payload with iat in the PAST
    mock_payload = {
        "sub": "1",
        "email": "test@example.com",
        "key": "some_uuid",
        "iat": past.timestamp(),
    }

    with (
        patch(
            "apps.auth.auth_handler.auth_handler.decode_token", new_callable=AsyncMock
        ) as mock_decode,
        patch(
            "services.redis_service.redis_service.get_cache", new_callable=AsyncMock
        ) as mock_redis_get,
        patch(
            "services.redis_service.redis_service.delete_cache", new_callable=AsyncMock
        ) as _,
        patch(
            "apps.users.crud.user_manager.get", new_callable=AsyncMock
        ) as mock_get_user,
    ):
        mock_decode.return_value = mock_payload
        mock_redis_get.return_value = "1"  # User ID stored in redis
        mock_get_user.return_value = mock_user

        # Call refresh endpoint with header
        headers = {"refresh-token": "old_refresh_token"}
        response = await client.post("/auth/refresh", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Session expired. Please re-authenticate."
