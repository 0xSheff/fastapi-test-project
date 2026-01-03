import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from unittest.mock import AsyncMock
from app_factory import get_application
from apps.core.dependencies import get_async_session

# Mock the database session/connection
@pytest.fixture
def mock_db_session():
    """
    Creates a mock database session.
    You can configure this mock in individual tests to return specific data.
    """
    session = AsyncMock()
    # Setup common mock behaviors here if needed, e.g.:
    # session.commit.return_value = None
    return session

@pytest.fixture
async def client(mock_db_session) -> AsyncGenerator[AsyncClient, None]:
    app = get_application()
    
    # Override the dependency that provides the DB session.
    app.dependency_overrides[get_async_session] = lambda: mock_db_session
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    # Clean up overrides after test
    app.dependency_overrides = {}
