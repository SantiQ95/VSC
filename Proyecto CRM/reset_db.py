# reset_db.py

from databases.db import usuarios_collection, facturas_collection
import os
from dotenv import load_dotenv

load_dotenv()
print("📡 ATLAS_URI from .env:", os.getenv("ATLAS_URI"))

# Reset Database Script
# This script connects to the MongoDB collections and allows the user to reset the database by deleting
def reset_database():
    print("🧪 Conectado a la colección usuarios:", usuarios_collection.full_name)
    print("🧪 Conectado a la colección facturas:", facturas_collection.full_name)

    confirm = input("¿Estás seguro que deseas borrar todo? (s/n): ").strip().lower()

    if confirm == "s":
        res1 = usuarios_collection.delete_many({})
        res2 = facturas_collection.delete_many({})
        print(f"✅ Eliminados {res1.deleted_count} usuarios.")
        print(f"✅ Eliminadas {res2.deleted_count} facturas.")
    else:
        print("🚫 Cancelado. No se modificó la base de datos.")

if __name__ == "__main__":
    reset_database()