import json
import os
from unittest.mock import patch
import pytest
import requests
from config import JSON_FILE_NAME
from fetch_prices import fetch_bitcoin_price_from_api, fetch_prices_data


pytestmark = pytest.mark.integration


def test_fetch_bitcoin_price_from_api():
    session = requests.Session()
    price = fetch_bitcoin_price_from_api(session)

    assert price is not None
    assert isinstance(price, float)
    assert price > 0


@patch("fetch_prices.time.sleep", return_value=None)  # skip sleeping
def test_fetch_prices_data(mock_sleep):
    prices_data = fetch_prices_data(2)

    assert isinstance(prices_data, list)
    assert len(prices_data) == 2

    for item in prices_data:
        assert "timestamp" in item
        assert "price" in item
        assert isinstance(item["price"], float)
        assert item["price"] > 0

    assert os.path.exists(JSON_FILE_NAME)
    with open(JSON_FILE_NAME, 'r') as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert len(data) >= 2



