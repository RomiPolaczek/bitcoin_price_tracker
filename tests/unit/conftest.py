import pytest


@pytest.fixture
def mock_prices_data():
    return [
        {"timestamp": "2025-05-19 20:56:54", "price": 105402.895},
        {"timestamp": "2025-05-19 20:57:54", "price": 105439.985}
    ]
