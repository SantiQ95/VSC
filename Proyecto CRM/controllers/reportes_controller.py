from databases.db import usuarios_collection, facturas_collection

# Reportes Controller
# This module provides functions to generate financial reports for users and invoices.
def mostrar_resumen_financiero():
    print("\n=== RESUMEN FINANCIERO ===")

    usuarios = list(usuarios_collection.find())
    if not usuarios:
        print("No hay usuarios registrados.\n")
        return

    total_facturas = 0
    ingresos_totales = 0
    ingresos_pagados = 0
    ingresos_pendientes = 0

    for usuario in usuarios:
        email = usuario["email"]
        nombre = f"{usuario['nombre']} {usuario['apellidos']}"
        facturas = list(facturas_collection.find({"email_cliente": email}))

        total = sum(f["monto"] for f in facturas)
        pagadas = sum(f["monto"] for f in facturas if f["estado"] == "Pagada")
        pendientes = sum(f["monto"] for f in facturas if f["estado"] == "Pendiente")

        print(f"\nUsuario: {nombre} ({email})")
        print(f"- Total facturas: {len(facturas)}")
        print(f"- Monto total: ${total:.2f}")
        print(f"- Facturas pagadas: ${pagadas:.2f}")
        print(f"- Facturas pendientes: ${pendientes:.2f}")

        total_facturas += len(facturas)
        ingresos_totales += total
        ingresos_pagados += pagadas
        ingresos_pendientes += pendientes

    print("\n--- RESUMEN GENERAL ---")
    print(f"Total usuarios: {len(usuarios)}")
    print(f"Total facturas emitidas: {total_facturas}")
    print(f"Ingresos totales: ${ingresos_totales:.2f}")
    print(f"Ingresos recibidos: ${ingresos_pagados:.2f}")
    print(f"Ingresos pendientes: ${ingresos_pendientes:.2f}\n")
