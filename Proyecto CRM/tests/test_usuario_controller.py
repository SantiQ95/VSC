import pymongo
from unittest.mock import patch
from models.usuario import Usuario

@patch("models.usuario.usuarios_collection")
@patch("builtins.print")
def test_guardar_usuario_duplicado_prints_error(mock_print, mock_usuarios):
    # Simulate existing users for ID generation
    mock_usuarios.count_documents.return_value = 0

    # Raise a fully constructed DuplicateKeyError when insert is attempted
    mock_usuarios.insert_one.side_effect = pymongo.errors.DuplicateKeyError(
        "E11000 duplicate key error collection: usuarios index: email_1 dup key: { : \"laura@test.com\" }"
    )

    usuario = Usuario(
        nombre="Laura",
        apellidos="Martínez",
        email="laura@test.com",
        telefono="123456789",
        direccion="Calle Luna 42"
    )

    resultado = usuario.guardar()

    # ✅ Confirm it returns False
    assert resultado is False

    # ✅ Confirm it prints the correct error message (stripped of line breaks)
    mock_print.assert_any_call("❌ Error: El email ya existe en la base de datos (índice único).")
