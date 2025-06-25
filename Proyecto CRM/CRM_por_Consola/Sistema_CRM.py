from datetime import datetime

class Usuario:
    def __init__(self, nombre, apellidos, email, telefono='', direccion=''):
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.fecha_registro = datetime.now().strftime("%d/%m/%Y")
        self.facturas = []

class Factura:
    contador_facturas = 1

    def __init__(self, descripcion, monto, estado):
        self.numero = f"FAC{Factura.contador_facturas:03d}"
        Factura.contador_facturas += 1
        self.fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.descripcion = descripcion
        self.monto = monto
        self.estado = estado