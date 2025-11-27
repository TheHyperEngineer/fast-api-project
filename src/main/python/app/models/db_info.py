"""
DBInfo Pydantic model for diagnostics and metadata responses.

This model captures the response from `/db-info` and documents what values are provided.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List


class DBInfo(BaseModel):
    """Database diagnostics information.

    Fields:
    - databases: list of database names available to the client
    - collections: list of collections for the configured database
    - collection_count: number of documents in the configured collection
    """

    databases: List[str] = Field(..., description="Available databases")
    collections: List[str] = Field(...,
                                   description="Collections in configured DB")
    collection_count: int = Field(...,
                                  description="Document count in configured collection")

    model_config = {
        "json_schema_extra": {
            "example": {"databases": ["admin", "local", "test"], "collections": ["medical"], "collection_count": 275}
        }
    }
