import json
import os
from unittest.mock import MagicMock, patch
import pytest
from config import JSON_FILE_NAME
from fetch_prices import fetch_bitcoin_price_from_api, fetch_prices_data, save_to_json_file


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.get.return_value.status_code = 200
    response.get.return_value.json.return_value = {"data": {"amount": "106574.53", "base": "BTC", "currency": "USD"}}
    return response


def test_fetch_bitcoin_price_from_api_success(mock_response):
    price = fetch_bitcoin_price_from_api(mock_response)
    assert price == 106574.53


def test_fetch_bitcoin_price_from_api_error(mock_response):
    mock_response.get.return_value.status_code = 500  # internal server error in the API
    price = fetch_bitcoin_price_from_api(mock_response)
    assert price is None


@patch('fetch_prices.save_to_json_file')
@patch("fetch_prices.time.sleep", return_value=None)
def test_fetch_prices_data(mock_save_to_json_file, mock_sleep, mock_response, monkeypatch):
    with patch("fetch_prices.requests.Session", return_value=mock_response):
        prices_data = fetch_prices_data(2)

        assert len(prices_data) == 2
        for item in prices_data:
            assert "timestamp" in item
            assert "price" in item
            assert prices_data[0]['price'] == 106574.53
            assert prices_data[1]['price'] == 106574.53

        assert mock_save_to_json_file.call_count == 2  # to make sure that this function gets called twice


def test_save_to_json_file(mock_prices_data):
    save_to_json_file(mock_prices_data)

    assert os.path.exists(JSON_FILE_NAME)

    with open(JSON_FILE_NAME, 'r') as f:
        saved_data = json.load(f)
        assert saved_data == mock_prices_data
    os.remove(JSON_FILE_NAME)

