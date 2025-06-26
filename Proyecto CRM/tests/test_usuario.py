from models.usuario import Usuario
from datetime import datetime

# Tests for the Usuario model
def test_usuario_to_dict_fields():
    usuario = Usuario("Laura", "Martínez", "laura@test.com", "123456789", "Calle Luna 42")
    datos = usuario.to_dict()

    assert datos["nombre"] == "Laura"
    assert datos["apellidos"] == "Martínez"
    assert datos["email"] == "laura@test.com"
    assert datos["telefono"] == "123456789"
    assert datos["direccion"] == "Calle Luna 42"
    assert isinstance(datos["fecha_registro"], datetime)
