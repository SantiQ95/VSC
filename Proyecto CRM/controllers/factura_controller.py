from models.factura import Factura
from databases.db import facturas_collection, usuarios_collection

# Factura Controller
# Handles the creation and retrieval of invoices in the system.
def crear_factura():
    print("\n=== CREAR FACTURA ===")
    email = input("Ingrese email del usuario: ").strip()
    usuario = usuarios_collection.find_one({"email": email})

    if not usuario:
        print("❌ Usuario no encontrado. No se puede crear factura.\n")
        return

    descripcion = input("Ingrese descripción del servicio/producto: ").strip()
    if not descripcion:
        print("❌ La descripción no puede estar vacía.\n")
        return

    monto = _solicitar_monto()
    if monto is None:
        return

    estado = _seleccionar_estado()
    if not estado:
        return

    factura = Factura(email, descripcion, monto, estado)
    factura.guardar()

    _mostrar_factura_creada(factura, usuario)

# ——— Mostrar facturas por usuario ———
# This function retrieves and displays all invoices for a specific user based on their email.
def mostrar_facturas_por_usuario():
    print("\n=== FACTURAS POR USUARIO ===")
    email = input("Ingrese email del usuario: ").strip()
    usuario = usuarios_collection.find_one({"email": email})

    if not usuario:
        print("❌ Usuario no encontrado.\n")
        return

    facturas = list(facturas_collection.find({"email_cliente": email}))

    if not facturas:
        print(f"El usuario {usuario['nombre']} no tiene facturas registradas.\n")
        return

    print(f"\n--- FACTURAS DE {usuario['nombre']} {usuario['apellidos']} ---")

    grouped = {"Pendiente": [], "Pagada": [], "Cancelada": []}
    total = 0
    estado_totales = {"Pendiente": 0, "Pagada": 0, "Cancelada": 0}

    for f in facturas:
        grouped[f["estado"]].append(f)
        total += f["monto"]
        estado_totales[f["estado"]] += f["monto"]

    for estado, lista in grouped.items():
        if lista:
            print(f"\n📂 Facturas {estado.upper()}:")
            for i, f in enumerate(lista, start=1):
                print(f"\nFactura #{i}")
                print(f"Número: {f['numero']}")
                print(f"Fecha de emisión: {f['fecha_emision']}")
                print(f"Descripción: {f['descripcion']}")
                print(f"Monto: ${f['monto']:.2f}")
                print(f"Estado: {f['estado']}")

    print(f"\n--- RESUMEN ---")
    print(f"Total de facturas: {len(facturas)}")
    print(f"Monto total facturado: ${total:.2f}")
    print(f"Monto pagado: ${estado_totales['Pagada']:.2f}")
    print(f"Monto pendiente: ${estado_totales['Pendiente']:.2f}")
    print(f"Monto cancelado: ${estado_totales['Cancelada']:.2f}\n")


# ——— Helpers ———
# These are utility functions used within the controller to handle user input and display messages.
# They help keep the main functions clean and focused on their primary tasks.
def _solicitar_monto():
    try:
        monto = float(input("Ingrese monto total: ").strip())
        if monto <= 0:
            raise ValueError
        return monto
    except ValueError:
        print("❌ Monto inválido. Debe ser un número positivo.\n")
        return None

# This function prompts the user to select an invoice status from a predefined list.
# It returns the selected status or None if the input is invalid.
def _seleccionar_estado():
    print("Seleccione estado:")
    print("1. Pendiente")
    print("2. Pagada")
    print("3. Cancelada")
    opcion = input("Estado: ").strip()

    estados = {"1": "Pendiente", "2": "Pagada", "3": "Cancelada"}
    estado = estados.get(opcion)

    if not estado:
        print("❌ Estado no válido.\n")
        return None

    return estado

# This function displays the details of the created invoice, including its number, issue date, client information, description, amount, and status.
# It provides a clear confirmation to the user that the invoice has been successfully created.
def _mostrar_factura_creada(factura, usuario):
    print(f"\n✅ Factura creada exitosamente!")
    print(f"Número: {factura.numero}")
    print(f"Fecha de emisión: {factura.fecha_emision}")
    print(f"Cliente: {usuario['nombre']} {usuario['apellidos']}")
    print(f"Descripción: {factura.descripcion}")
    print(f"Monto: ${factura.monto:.2f}")
    print(f"Estado: {factura.estado}\n")
