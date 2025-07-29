import pytest
from unittest.mock import MagicMock, create_autospec, patch
from app.Service.TwilioServiceImp import TwilioServiceImp
from app.Model.TwilioModel import TwilioModel
from app.Repository.TwilioRepository import TwilioRepository

class TestTwilioServiceImp:
    @pytest.fixture(autouse=True)
    def mock_twilio(self):
        with patch('app.Repository.TwilioRepository.Client') as mock_twilio_client:
            mock_instance = MagicMock()
            mock_instance.messages.create.return_value = MagicMock(sid="dummy_sid")
            mock_twilio_client.return_value = mock_instance
            yield

    @pytest.fixture
    def mock_repo(self):
        return create_autospec(TwilioRepository)

    @pytest.fixture
    def service(self, mock_repo):
        return TwilioServiceImp(repo=mock_repo)

    @pytest.fixture
    def sample_twilio(self):
        return TwilioModel(
            numero="+123456789",
            mensaje="Test message"
        )

    def test_enviar_mensaje_valido(self, service, mock_repo, sample_twilio):
        # Arrange
        mock_repo.enviar_mensaje.return_value = True
        
        # Act
        result = service.enviar_mensaje(sample_twilio)
        
        # Assert
        assert "Mensaje enviado al numero" in result
        mock_repo.enviar_mensaje.assert_called_once_with("+123456789", "Test message")
