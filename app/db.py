import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# default to test or rag_vector_db
MONGO_DB = os.getenv("MONGO_DB", "test")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "medical")

client = AsyncIOMotorClient(MONGO_URI)
database = client[MONGO_DB]
collection = database[MONGO_COLLECTION]
