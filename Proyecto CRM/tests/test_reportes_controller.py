import pymongo
from unittest.mock import patch
from controllers import reportes_controller

# Test resumen financiero por usuario
@patch("controllers.reportes_controller.usuarios_collection")
@patch("controllers.reportes_controller.facturas_collection")
# Mocking the database collections for users and invoices
def test_resumen_financiero_multi_usuario(mock_facturas, mock_usuarios):
    mock_usuarios.find.return_value = [
        {"nombre": "Ana", "apellidos": "López", "email": "ana@test.com"},
        {"nombre": "Luis", "apellidos": "Pérez", "email": "luis@test.com"},
        {"nombre": "Sofía", "apellidos": "Ramírez", "email": "sofia@test.com"},
    ]

    # Mocking the find method for invoices based on user email
    # This simulates the database returning different invoices for each user
    def fake_find(query):
        email = query.get("email_cliente", "")
        if email == "ana@test.com":
            return [
                {"monto": 100.0, "estado": "Pagada"},
                {"monto": 50.0, "estado": "Pendiente"},
            ]
        elif email == "luis@test.com":
            return [
                {"monto": 200.0, "estado": "Pagada"},
                {"monto": 100.0, "estado": "Cancelada"},
            ]
        elif email == "sofia@test.com":
            return []
        return []

    mock_facturas.find.side_effect = fake_find

    with patch("builtins.print") as mock_print:
        reportes_controller.mostrar_resumen_financiero()

        printed = [str(call) for call in mock_print.call_args_list]

        # Match key output patterns — less brittle than exact lines
        assert any("Monto total: $150.00" in call for call in printed)
        assert any("Facturas pagadas: $100.00" in call for call in printed)
        assert any("Facturas pendientes: $50.00" in call for call in printed)

        assert any("Monto total: $300.00" in call for call in printed)
        assert any("Facturas pagadas: $200.00" in call for call in printed)

        assert any("Monto total: $0.00" in call for call in printed)

        assert any("Total facturas emitidas: 4" in call for call in printed)
        assert any("Ingresos totales: $450.00" in call for call in printed)
        assert any("Ingresos recibidos: $300.00" in call for call in printed)
        assert any("Ingresos pendientes: $50.00" in call for call in printed)
