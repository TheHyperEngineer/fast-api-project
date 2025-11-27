import os
from typing import Optional
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "test")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "medical")

_client: Optional[AsyncIOMotorClient] = None
_database = None
_collection = None

async def init_db(app: FastAPI):
    global _client, _database, _collection
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URI)
        _database = _client[MONGO_DB]
        _collection = _database[MONGO_COLLECTION]
        app.state.mongo_client = _client
        app.state.db = _database
        app.state.collection = _collection

async def close_db(app: FastAPI):
    global _client, _database, _collection
    if _client is not None:
        _client.close()
        _client = None
        _database = None
        _collection = None
    if hasattr(app.state, "mongo_client"):
        delattr(app.state, "mongo_client")
    if hasattr(app.state, "db"):
        delattr(app.state, "db")
    if hasattr(app.state, "collection"):
        delattr(app.state, "collection")

def get_client() -> Optional[AsyncIOMotorClient]:
    return _client

def get_database():
    return _database

def get_collection():
    return _collection

async def find_items(limit: int = 100):
    coll = get_collection()
    if coll is None:
        raise RuntimeError("collection not initialized")
    docs = await coll.find().to_list(limit)
    return docs