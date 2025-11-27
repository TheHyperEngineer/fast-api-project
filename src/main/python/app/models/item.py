"""
Item Pydantic model.
This module defines application data models (similar to DTOs or entities in Java/Spring).

Purpose and mapping for a Spring Boot developer:
 - In Spring Boot you'd have `domain` or `model` classes annotated with `@Entity` or DTOs for API.
 - Here, `pydantic.BaseModel` provides the validation and serialization for the API.

This file contains a simple `Item` model used by the `/items` endpoint. The `_id` alias maps to
the MongoDB ObjectId (converted to string in the controller); we expose it as `id` for JSON.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class Item(BaseModel):
    """Pydantic model for items stored in MongoDB.

    Fields:
    - id: Identifier as string (converted from MongoDB ObjectId)
    - name: Example name for item
    - value: Optional integer value
    """

    id: Optional[str] = Field(
        None, alias="_id", description="ID of the document (converted to string)")
    name: str = Field(..., description="Name of item")
    value: Optional[int] = Field(None, description="Optional numeric value")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {"_id": "655647c5f9d7b6b7f8d2afe7", "name": "sample", "value": 42}
        },
    }
