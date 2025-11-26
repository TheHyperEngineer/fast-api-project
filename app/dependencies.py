import os
from fastapi import Depends, Header, HTTPException
from typing import Optional

from .db import client, database, collection

API_KEY = os.getenv("API_KEY")


async def get_client():
    return client


async def get_database():
    return database


async def get_collection():
    return collection


async def api_key_required(x_api_key: Optional[str] = Header(None)):
    """Simple API key check. If `API_KEY` is not set, API is unprotected."""
    if API_KEY is None:
        return True
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
