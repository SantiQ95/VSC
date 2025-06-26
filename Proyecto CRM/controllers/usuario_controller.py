import re
from models.usuario import Usuario
from databases.db import usuarios_collection

# Usuario Controller
# This module provides functions to register, search, and display users in the system.

def registrar_usuario():
    print("\n=== REGISTRO DE NUEVO USUARIO ===")

    nombre = input("Ingrese nombre: ").strip()
    apellidos = input("Ingrese apellidos: ").strip()
    email = input("Ingrese email: ").strip()

    if not _campos_obligatorios_validos(nombre, apellidos, email):
        return

    if not _email_valido(email):
        print("❌ Email no tiene un formato válido.\n")
        return

    if usuarios_collection.find_one({"email": email}):
        print("❌ Ya existe un usuario con ese email.\n")
        return

    telefono = input("Ingrese teléfono (opcional): ").strip()
    direccion = input("Ingrese dirección (opcional): ").strip()

    usuario = Usuario(nombre, apellidos, email, telefono, direccion)
    usuario.guardar()

    print(f"\n✅ Usuario registrado exitosamente!")
    print(f"ID asignado: {usuario.id}")
    print(f"Fecha de registro: {usuario.fecha_registro}\n")


def buscar_usuario():
    print("\n=== BUSCAR USUARIO ===")
    print("1. Buscar por email")
    print("2. Buscar por nombre")
    opcion = input("Seleccione método de búsqueda: ").strip()

    if opcion == "1":
        criterio = input("Ingrese email: ").strip()
        usuario = usuarios_collection.find_one({"email": criterio})
    elif opcion == "2":
        criterio = input("Ingrese nombre: ").strip()
        usuario = usuarios_collection.find_one({
            "nombre": {"$regex": criterio, "$options": "i"}
        })
    else:
        print("❌ Opción no válida.\n")
        return

    _mostrar_usuario(usuario)


def mostrar_todos_usuarios():
    print("\n=== LISTA DE USUARIOS ===")
    usuarios = list(usuarios_collection.find())

    if not usuarios:
        print("No hay usuarios registrados.\n")
        return

    for i, u in enumerate(usuarios, start=1):
        print(f"\nUsuario #{i}")
        print(f"ID: {u['id']}")
        print(f"Nombre: {u['nombre']} {u['apellidos']}")
        print(f"Email: {u['email']}")
        print(f"Teléfono: {u.get('telefono', 'No especificado')}")
        print(f"Fecha de registro: {u['fecha_registro']}")

    print(f"\nTotal de usuarios registrados: {len(usuarios)}\n")


# ——— Helpers ———

def _campos_obligatorios_validos(nombre, apellidos, email):
    if not nombre or not apellidos or not email:
        print("❌ Nombre, apellidos y email son obligatorios.\n")
        return False
    return True

def _email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def _mostrar_usuario(usuario):
    if not usuario:
        print("❌ Usuario no encontrado.\n")
        return

    print("\n--- USUARIO ENCONTRADO ---")
    print(f"ID: {usuario['id']}")
    print(f"Nombre: {usuario['nombre']} {usuario['apellidos']}")
    print(f"Email: {usuario['email']}")
    print(f"Teléfono: {usuario.get('telefono', 'No especificado')}")
    print(f"Dirección: {usuario.get('direccion', 'No especificado')}")
    print(f"Fecha de registro: {usuario['fecha_registro']}\n")
