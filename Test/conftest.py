import pytest
import os
from unittest.mock import patch

@pytest.fixture(autouse=True, scope="session")
def mock_env_vars():
    with patch.dict(os.environ, {
        # Variables para Usuario, Notificacion y Pedido
        "MYSQL_HOST": "localhost",
        "MYSQL_USER": "user_test",
        "MYSQL_PASSWORD": "pass_test",
        "MYSQL_DATABASE": "db_test",

        # Variables para Twilio
        "twilio_account_sid": "fake_sid",
        "twilio_auth_token": "fake_token",
        "twilio_phone_number": "+123456789"
    }, clear=False):
        yield
