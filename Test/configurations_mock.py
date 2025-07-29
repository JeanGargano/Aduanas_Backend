# tests/conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    # Crea un mock de Settings con valores falsos
    mock_settings = MagicMock(spec=Settings)
    mock_settings.MYSQL_HOST = "localhost"
    mock_settings.MYSQL_USER = "test_user"
    mock_settings.MYSQL_PASSWORD = "test_pass"
    mock_settings.MYSQL_DATABASE = "test_db"
    mock_settings.TWILIO_ACCOUNT_SID = "test_sid"
    mock_settings.TWILIO_AUTH_TOKEN = "test_token"
    mock_settings.TWILIO_PHONE_NUMBER = "+1234567890"

    # Reemplaza la instancia real de `settings` con el mock
    monkeypatch.setattr("configurations.settings", mock_settings)