import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from unittest.mock import MagicMock
from app_factory import get_application

# Mock the database session/connection
@pytest.fixture
def mock_db_session():
    """
    Creates a mock database session.
    """
    session = MagicMock()
    # Setup common mock behaviors here if needed, e.g.:
    # session.commit.return_value = None
    return session

@pytest.fixture
async def client(mock_db_session) -> AsyncGenerator[AsyncClient, None]:
    app = get_application()
    
    # Here you would typically override the dependency that provides the DB session.
    # Example:
    # app.dependency_overrides[get_db] = lambda: mock_db_session
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    # Clean up overrides after test
    app.dependency_overrides = {}
