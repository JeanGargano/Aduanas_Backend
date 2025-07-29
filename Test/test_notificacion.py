import pytest
from unittest.mock import MagicMock, create_autospec
from app.Service.NotificacionServiceImp import NotificacionServiceImp
from app.Model.NotificacionModel import NotificacionModel
from app.Repository.NotificacionRepository import NotificacionRepository

class TestNotificacionServiceImp:
    @pytest.fixture
    def mock_repo(self):
        return create_autospec(NotificacionRepository)

    @pytest.fixture
    def service(self, mock_repo):
        return NotificacionServiceImp(repo=mock_repo)

    @pytest.fixture
    def sample_notificacion(self):
        return NotificacionModel(
            usuario_id=1,
            pedido_id=1,
            mensaje="Test message"
        )

    def test_crear_notificacion_valida(self, service, mock_repo, sample_notificacion):
        # Arrange
        mock_repo.crear_notificacion.return_value = sample_notificacion
        
        # Act
        result = service.crear_notificacion(sample_notificacion)
        
        # Assert
        assert result == sample_notificacion
        mock_repo.crear_notificacion.assert_called_once_with(sample_notificacion)

    def test_listar_notificaciones(self, service, mock_repo, sample_notificacion):
        # Arrange
        mock_repo.listar_notificaciones.return_value = [sample_notificacion]
        
        # Act
        result = service.listar_notificaciones()
        
        # Assert
        assert len(result) == 1
        assert result[0] == sample_notificacion
        mock_repo.listar_notificaciones.assert_called_once()

   

    def test_listar_mis_notificaciones(self, service, mock_repo, sample_notificacion):
        # Arrange
        mock_repo.listar_mis_notificaciones.return_value = [sample_notificacion]
        
        # Act
        result = service.listar_mis_notificaciones(1)
        
        # Assert
        assert len(result) == 1
        assert result[0] == sample_notificacion
        mock_repo.listar_mis_notificaciones.assert_called_once_with(1)

