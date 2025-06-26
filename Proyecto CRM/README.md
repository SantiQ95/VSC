CRM Console App (Python + MongoDB)

A lightweight, command-line CRM tool built with Python and MongoDB. Register users, generate invoices, view financial summaries, and run searches — all through a clean and modular console interface.

Features:

User registration and validation

Invoice creation with status tracking

User search by name or email

Per-user invoice summary reports

Financial breakdowns grouped by status

In-memory and mock data generation with Faker

Test coverage via pytest

Project Structure:

crm-console/ ├── controllers/ │ ├── usuario_controller.py │ └── factura_controller.py ├── models/ │ ├── usuario.py │ └── factura.py ├── databases/ │ ├── db.py │ └── generate_data.py ├── tests/ │ ├── test_usuarios.py │ └── test_facturas.py ├── main.py ├── requirements.txt └── README.md

Requirements:

Python 3.10 or higher

MongoDB (local or remote instance)

Dependencies listed in requirements.txt

Install dependencies with:

pip install -r requirements.txt

Generate Sample Data:

Populate your database with 20–30 random users and 0–5 invoices per user:

Run this command from the project root:

python -m databases.generate_data

Run the Application:

From the root folder:

python main.py

This launches the interactive CRM menu via your terminal.

Design Notes:

Data Models:

Usuario: ID (e.g. USR001), name, email, phone, address, registration datetime

Factura: Invoice number (e.g. FAC001), client email, description, amount, status, emission datetime

Models auto-generate identifiers and format data consistently.

Tech Stack:

Python

PyMongo

Faker

Pytest

Tips:

If a reset_db.py script is included, use it to wipe sample data

Store sensitive DB info in a .env file

Run tests using: pytest tests/