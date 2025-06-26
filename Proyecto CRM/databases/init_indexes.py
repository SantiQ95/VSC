from databases.db import usuarios_collection

# Unique Index Creation
# This function creates a unique index on the "email" field of the usuarios_collection.
def crear_indices_unicos():
    usuarios_collection.create_index("email", unique=True)