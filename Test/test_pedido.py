import pytest
from unittest.mock import create_autospec, patch
from app.Service.PedidoServiceImp import PedidoServiceImp
from app.Model.PedidoModel import PedidoModel
from app.Repository.PedidoRepository import PedidoRepository
from datetime import date

class TestPedidoServiceImp:
    @pytest.fixture(autouse=True)
    def mock_dependencies(self):
        with patch('app.configurations.settings') as mock_settings:
            mock_settings.MYSQL_HOST = "localhost"
            mock_settings.MYSQL_USER = "test_user"
            mock_settings.MYSQL_PASSWORD = "test_password"
            mock_settings.MYSQL_DATABASE = "test_db"
            yield

    @pytest.fixture
    def mock_repo(self):
        return create_autospec(PedidoRepository)

    @pytest.fixture
    def service(self, mock_repo):
        return PedidoServiceImp(repo=mock_repo)

    @pytest.fixture
    def sample_pedido(self):
        return PedidoModel(
            id_cliente=1,
            fecha_arribo=date.today(),
            estado="EN PROCESO"
        )

    def test_crear_pedido_valido(self, service, mock_repo, sample_pedido):
        mock_repo.crear_pedido.return_value = True
        result = service.crear_pedido(sample_pedido)
        assert result == "Pedido creado exitosamente"
        mock_repo.crear_pedido.assert_called_once_with(sample_pedido)


    def test_listar_pedidos(self, service, mock_repo, sample_pedido):
        mock_repo.listar_pedidos.return_value = [sample_pedido]
        result = service.listar_pedidos()
        assert len(result) == 1
        assert result[0] == sample_pedido
        mock_repo.listar_pedidos.assert_called_once()


    def test_listar_pedidos_del_cliente(self, service, mock_repo, sample_pedido):
        mock_repo.listar_pedidos_del_cliente.return_value = [sample_pedido]
        result = service.listar_pedidos_del_cliente(1)
        assert len(result) == 1
        assert result[0] == sample_pedido
        mock_repo.listar_pedidos_del_cliente.assert_called_once_with(1)

    def test_listar_pedido_por_id(self, service, mock_repo, sample_pedido):
        mock_repo.listar_pedido_por_id.return_value = [sample_pedido]
        result = service.listar_pedido_por_id(1)
        assert len(result) == 1
        assert result[0] == sample_pedido
        mock_repo.listar_pedido_por_id.assert_called_once_with(1)


    def test_actualizar_pedido_por_id(self, service, mock_repo):
        mock_repo.actualizar_pedido_por_id.return_value = True
        datos = {"estado": "COMPLETADO"}
        result = service.actualizar_pedido_por_id(1, datos)
        assert result is True
        mock_repo.actualizar_pedido_por_id.assert_called_once_with(1, datos)
