from unittest.mock import patch, MagicMock
from email_service import send_max_price_email


@patch("smtplib.SMTP")
def test_send_max_price_email(mock_smtp, mock_prices_data):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    result = send_max_price_email(mock_prices_data)
    assert result is True
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()

    msg = mock_server.send_message.call_args[0][0]
    assert "Bitcoin Price Report - Maximum Price" in msg["Subject"]
    assert "$105,439.99" in msg.get_payload()
    assert "2025-05-19 20:57:54" in msg.get_payload()


@patch("smtplib.SMTP")
def test_send_max_price_email_error(mock_smtp, mock_prices_data):
    mock_smtp.return_value.__enter__.side_effect = Exception(
        "connection failed"
    )  # result is false on exception
    result = send_max_price_email(mock_prices_data)
    assert result is False
