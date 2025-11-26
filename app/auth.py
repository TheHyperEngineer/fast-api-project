from fastapi import Depends, Header, HTTPException
from typing import Optional
import os

API_KEY = os.getenv("API_KEY")


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> bool:
    if API_KEY is None:
        return True
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
