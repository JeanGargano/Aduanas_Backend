import pytest
from unittest.mock import create_autospec
from app.Service.UsuarioServiceImp import UsuarioServiceImp, verificar_password
from app.Model.UsuarioModel import UsuarioModel
from app.Repository.UsuarioRepository import UsuarioRepository
import bcrypt

class TestUsuarioServiceImp:
    @pytest.fixture
    def mock_repo(self):
        return create_autospec(UsuarioRepository)

    @pytest.fixture
    def service(self, mock_repo):
        return UsuarioServiceImp(repo=mock_repo)

    @pytest.fixture
    def sample_usuario(self):
        return UsuarioModel(
            identificacion=123,
            nombre="Test User",
            correo="test@example.com",
            celular=1234567890
        )

    def test_verificar_password(self):
        # Arrange
        plain = "password123"
        hashed = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Act & Assert
        assert verificar_password(plain, hashed) is True
        assert verificar_password("wrong", hashed) is False

    def test_crear_usuario_valido(self, service, mock_repo, sample_usuario):
        # Arrange
        mock_repo.buscar_usuario.return_value = None
        mock_repo.crear_usuario.return_value = None
        
        # Act
        result = service.crear_usuario(sample_usuario)
        
        # Assert
        assert result == "Usuario creado exitosamente"
        mock_repo.buscar_usuario.assert_called_once_with(123)
        mock_repo.crear_usuario.assert_called_once_with(sample_usuario)



    def test_listar_usuarios(self, service, mock_repo, sample_usuario):
        # Arrange
        mock_repo.listar_usuarios.return_value = [sample_usuario]
        
        # Act
        result = service.listar_usuarios()
        
        # Assert
        assert len(result) == 1
        assert result[0] == sample_usuario
        mock_repo.listar_usuarios.assert_called_once()

    def test_listar_usuario_por_id(self, service, mock_repo, sample_usuario):
        # Arrange
        mock_repo.listar_usuario_por_id.return_value = [sample_usuario]
        
        # Act
        result = service.listar_usuario_por_id(123)
        
        # Assert
        assert len(result) == 1
        assert result[0] == sample_usuario
        mock_repo.listar_usuario_por_id.assert_called_once_with(123)


    def test_actualizar_usuario_por_id(self, service, mock_repo):
        # Arrange
        mock_repo.actualizar_usuario_por_id.return_value = True
        datos = {"nombre": "Nuevo Nombre"}
        
        # Act
        result = service.actualizar_usuario_por_id(123, datos)
        
        # Assert
        assert result is True
        mock_repo.actualizar_usuario_por_id.assert_called_once_with(123, datos)


    def test_asignar_contraseña(self, service, mock_repo):
        # Arrange
        mock_repo.buscar_usuario.return_value = {"identificacion": 123}
        mock_repo.asignar_contraseña.return_value = True
        
        # Act
        result = service.asignar_contraseña(123, "newpass")
        
        # Assert
        assert result is True
        mock_repo.asignar_contraseña.assert_called_once()


    def test_logear_usuario_fallido(self, service, mock_repo):
        # Arrange
        hashed = bcrypt.hashpw("correct".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        mock_repo.buscar_usuario.return_value = {
            "identificacion": 123,
            "nombre": "Test",
            "correo": "test@example.com",
            "contraseña": hashed
        }
        
        # Act & Assert
        with pytest.raises(ValueError):
            service.logear_usuario(123, "wrong")