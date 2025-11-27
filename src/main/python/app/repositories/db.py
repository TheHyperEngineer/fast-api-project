import os
from motor.motor_asyncio import AsyncIOMotorClient

"""
Repository module for MongoDB connection.

Purpose and mapping for a Spring Boot developer:
 - In Spring Boot you'd configure a `MongoClient` bean in a `@Configuration` class or use `spring.data.mongodb` settings.
 - This Python module creates an AsyncIO Motor client and provides `client`, `database` and `collection` objects for other modules.

Note:
 - Configuration values (URI, DB name, and collection) are read from environment variables and default to local values for development.
 - Using a module-level `client` means the same instance can be imported and shared across modules (similar to a singleton bean).
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Environment-configurable values; these can be changed at runtime with environment variables.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "test")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "medical")

# Create the AsyncIO Motor client instance. This is safe to import across modules and will lazily connect on first use.
client = AsyncIOMotorClient(MONGO_URI)
database = client[MONGO_DB]
collection = database[MONGO_COLLECTION]


client = AsyncIOMotorClient(MONGO_URI)
database = client[MONGO_DB]
collection = database[MONGO_COLLECTION]
