from datetime import datetime
from databases.db import facturas_collection
import re

# Factura Model
# This class represents an invoice in the CRM system.
class Factura:
    # Represents an invoice in the CRM system.
    # Each invoice has a unique number, client email, description, amount, status, and issue date.
    # The invoice number is automatically generated based on the total number of invoices in the collection.
    def __init__(self, email_cliente: str, descripcion: str, monto: float, estado: str):
        self.numero: str = self._generar_numero_factura()
        self.email_cliente: str = email_cliente.lower().strip()
        self.descripcion: str = descripcion.strip()[:100]
        self.monto: float = round(monto, 2)
        self.estado: str = estado  # Should be validated before instantiating
        self.fecha_emision: datetime = datetime.now()

    # Generates a unique invoice number based on the total count of invoices in the collection.
    # The format is "FAC" followed by a three-digit number (e.g., FAC
    def _generar_numero_factura(self) -> str:
        total = facturas_collection.count_documents({})
        return f"FAC{total + 1:03d}"

    # Converts the invoice object to a dictionary representation for easy storage in the database.
    # This method is used to prepare the invoice data for insertion into the MongoDB collection.
    def to_dict(self) -> dict:
        return {
            "numero": self.numero,
            "email_cliente": self.email_cliente,
            "descripcion": self.descripcion,
            "monto": self.monto,
            "estado": self.estado,
            "fecha_emision": self.fecha_emision
        }

    # Saves the invoice to the MongoDB collection.
    # This method inserts the invoice data into the `facturas` collection in the database.
    def guardar(self):
        facturas_collection.insert_one(self.to_dict())
