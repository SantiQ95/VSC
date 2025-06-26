import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Ensure the path is correct relative to this script's location
load_dotenv(dotenv_path="../.env")


uri = os.getenv("ATLAS_URI")
print("📦 Loaded URI:", uri)  # Print what was actually read

# Now try the connection
from pymongo import MongoClient
client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print("❌ Connection failed:", e)
