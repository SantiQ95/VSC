import random
from faker import Faker
from models.usuario import Usuario
from models.factura import Factura

# Faker config for Spanish names/addresses
fake = Faker("es_ES")

# Predefined options
ESTADOS_FACTURA = ["Pendiente", "Pagada", "Cancelada"]
DESCRIPCIONES = [
    "Consultoría de negocio",
    "Servicio de soporte técnico",
    "Mantenimiento mensual",
    "Desarrollo web",
    "Formación personalizada",
    "Auditoría de procesos",
    "Implementación de sistema CRM",
]

# Function to populate the database with random users and invoices
# This function generates a random number of users (between 20 and 30) and for each user, it creates a random number of invoices (between 0 and 5).
# Each invoice has a random description, amount, and status.
def poblar_base_datos():
    num_usuarios = random.randint(20, 30)
    print(f"🧑 Generando {num_usuarios} usuarios y facturas...\n")

    for i in range(1, num_usuarios + 1):
        nombre = fake.first_name()
        apellidos = fake.last_name()
        email = f"{nombre.lower()}.{apellidos.lower()}{random.randint(100, 999)}@email.com"
        telefono = fake.phone_number()
        direccion = fake.address().replace("\n", ", ")

        usuario = Usuario(nombre, apellidos, email, telefono, direccion)
        usuario.guardar()

        num_facturas = random.randint(0, 5)
        print(f"  🔹 Usuario {usuario.id}: {usuario.nombre} {usuario.apellidos} → {num_facturas} factura(s)")

        for _ in range(num_facturas):
            factura = Factura(
                email_cliente=usuario.email,
                descripcion=random.choice(DESCRIPCIONES),
                monto=round(random.uniform(50.0, 1000.0), 2),
                estado=random.choice(ESTADOS_FACTURA)
            )
            factura.guardar()

    print("\n✅ Base de datos poblada exitosamente.")

if __name__ == "__main__":
    poblar_base_datos()
