from models.factura import Factura
from datetime import datetime

# Tests for the Factura model
def test_factura_to_dict_fields():
    factura = Factura("laura@test.com", "Servicio de mantenimiento", 199.99, "Pagada")
    datos = factura.to_dict()

    assert datos["email_cliente"] == "laura@test.com"
    assert datos["descripcion"] == "Servicio de mantenimiento"
    assert datos["monto"] == 199.99
    assert datos["estado"] == "Pagada"
    assert datos["numero"].startswith("FAC")
    assert isinstance(datos["fecha_emision"], datetime)
