from unittest.mock import patch, MagicMock
from controllers import factura_controller
from models.factura import Factura


@patch("controllers.factura_controller.usuarios_collection")
def test_crear_factura_usuario_no_encontrado(mock_usuarios):
    mock_usuarios.find_one.return_value = None

    inputs = ["correo@falso.com"]
    with patch("builtins.input", side_effect=inputs), \
         patch("builtins.print") as mock_print:
        factura_controller.crear_factura()
        mock_print.assert_any_call("❌ Usuario no encontrado. No se puede crear factura.\n")


@patch("controllers.factura_controller.usuarios_collection")
def test_crear_factura_descripcion_vacia(mock_usuarios):
    mock_usuarios.find_one.return_value = {"email": "valido@test.com"}

    inputs = ["valido@test.com", ""]
    with patch("builtins.input", side_effect=inputs), \
         patch("builtins.print") as mock_print:
        factura_controller.crear_factura()
        mock_print.assert_any_call("❌ La descripción no puede estar vacía.\n")


@patch("controllers.factura_controller.usuarios_collection")
def test_crear_factura_monto_invalido(mock_usuarios):
    mock_usuarios.find_one.return_value = {"email": "valido@test.com"}

    inputs = [
        "valido@test.com",      # email
        "Servicio X",           # descripcion
        "-500",                 # monto inválido
    ]

    with patch("builtins.input", side_effect=inputs), \
         patch("builtins.print") as mock_print:
        factura_controller.crear_factura()
        mock_print.assert_any_call("❌ Monto inválido. Debe ser un número positivo.\n")


@patch("controllers.factura_controller.usuarios_collection")
def test_crear_factura_estado_invalido(mock_usuarios):
    mock_usuarios.find_one.return_value = {"email": "valido@test.com"}

    inputs = [
        "valido@test.com",      # email
        "Servicio Y",           # descripcion
        "150.00",               # monto
        "7"                     # estado inválido
    ]

    with patch("builtins.input", side_effect=inputs), \
         patch("builtins.print") as mock_print:
        factura_controller.crear_factura()
        mock_print.assert_any_call("❌ Estado no válido.\n")


@patch("models.factura.Factura.guardar")
@patch("controllers.factura_controller.usuarios_collection")
def test_crear_factura_exitosa(mock_usuarios, mock_guardar):
    mock_usuarios.find_one.return_value = {
        "nombre": "Sara", "apellidos": "Delgado", "email": "sara@test.com"
    }

    inputs = [
        "sara@test.com",        # email
        "Diseño gráfico",       # descripcion
        "200.00",               # monto
        "2"                     # estado: Pagada
    ]

    with patch("builtins.input", side_effect=inputs), \
         patch("builtins.print") as mock_print:
        factura_controller.crear_factura()
        mock_guardar.assert_called_once()
        mock_print.assert_any_call("\n✅ Factura creada exitosamente!")



@patch("controllers.factura_controller.usuarios_collection")
def test_mostrar_facturas_usuario_no_encontrado(mock_usuarios):
    mock_usuarios.find_one.return_value = None

    with patch("builtins.input", return_value="fantasma@test.com"), \
         patch("builtins.print") as mock_print:
        factura_controller.mostrar_facturas_por_usuario()
        mock_print.assert_any_call("❌ Usuario no encontrado.\n")


@patch("controllers.factura_controller.facturas_collection")
@patch("controllers.factura_controller.usuarios_collection")
def test_mostrar_facturas_usuario_sin_facturas(mock_usuarios, mock_facturas):
    mock_usuarios.find_one.return_value = {
        "nombre": "Mario", "apellidos": "Pérez", "email": "mario@test.com"
    }
    mock_facturas.find.return_value = []

    with patch("builtins.input", return_value="mario@test.com"), \
         patch("builtins.print") as mock_print:
        factura_controller.mostrar_facturas_por_usuario()
        mock_print.assert_any_call("El usuario Mario no tiene facturas registradas.\n")
