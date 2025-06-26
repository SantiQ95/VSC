from datetime import datetime
from databases.db import usuarios_collection
import pymongo
import re

# Usuario Model
# This class represents a user in the CRM system.
class Usuario:
    # Represents a user in the CRM system.
    # Each user has a unique ID, name, surname, email, phone number, address, and registration date.
    # The ID is automatically generated based on the total number of users in the collection.
    def __init__(self, nombre: str, apellidos: str, email: str, telefono: str = '', direccion: str = ''):
        self.id: str = self._generar_id()  # e.g. USR001
        self.nombre: str = nombre.strip()[:30]
        self.apellidos: str = apellidos.strip()[:50]
        self.email: str = email.lower().strip()
        self.telefono: str = self._formatear_telefono(telefono)
        self.direccion: str = direccion.strip()[:100]
        self.fecha_registro: datetime = datetime.now()

    # Generates a unique user ID based on the total count of users in the collection.
    # The format is "USR" followed by a three-digit number (e.g., USR001, USR002).
    # This method ensures that each user has a distinct identifier.
    def _generar_id(self) -> str:
        total = usuarios_collection.count_documents({})
        return f"USR{total + 1:03d}"

    # Validates the required fields for user registration.
    # This method checks if the name, surname, and email are provided and not empty.
    def _formatear_telefono(self, numero: str) -> str:
        # Remove everything but digits and allow leading "+"
        numero = numero.strip().replace(" ", "")
        if numero.startswith("+"):
            return "+" + re.sub(r"\D", "", numero)
        return re.sub(r"\D", "", numero)

    # Converts the user object to a dictionary representation for easy storage in the database.
    # This method is used to prepare the user data for insertion into the MongoDB collection.
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_registro": self.fecha_registro
        }

    # Saves the user to the MongoDB collection.
    # This method inserts the user data into the `usuarios` collection in the database.
    def guardar(self) -> bool:
        try:
            usuarios_collection.insert_one(self.to_dict())
            print("✅ Usuario guardado correctamente en la base de datos.")
            return True
        except pymongo.errors.DuplicateKeyError:
            print("❌ Error: El email ya existe en la base de datos (índice único).")
            return False
        except Exception as e:
            print(f"⚠️ Error inesperado al guardar usuario: {e}")
            return False
