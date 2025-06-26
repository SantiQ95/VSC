
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
# Ensure the path is correct relative to this script's location
load_dotenv()

uri = os.getenv("ATLAS_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["EvolveCRM"]
usuarios_collection = db["usuarios"]
facturas_collection = db["facturas"]
