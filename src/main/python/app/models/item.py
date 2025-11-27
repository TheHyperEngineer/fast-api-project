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

    id: str = Field(None, alias="_id",
                    description="ID of the document (converted to string)")
    abstractId: int = Field(None, alias="ABSTRACT_ID",
                            description="Abstract Id of the item.")
    text: Optional[str] = Field(
        None, alias="TEXT", description="Text Value of the item")
    location: Optional[int] = Field(
        None, alias="LOCATION", description="Location Value of the item")
    label: Optional[str] = Field(
        None, alias="LABEL", description="Label of the item")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": {
                    "$oid": "691aa4383876ea26f51a7df5"
                },
                "ABSTRACT_ID": 2069316,
                "TEXT": "we developed an animal model of chronic allergic airway disease by repeatedly exposing nine sheep to tracheal instillation of ascaris antigen until stable increase in RL at three times control in six reactive sheep group c was obtained they were then compared to the three nonreactive sheep group b and a control group of eight sheep exposed to saline only group a in terms of pulmonary CF tests and bronchoalveolar lavage bal analyses RL was cm holsec in group a in group b and in group c trapping volume FRC by plethysmography and by helium rebreathing technique was l in group a in group b and in group c UP resistance at PF did not differ between any two CG but UP resistance near residual volume was cm holsec in a in b and in c in bal total cells were x ml in a in b and in c macrophages in bal were in a in b and in c neutrophils were in a in b in c eosinophils were in a in b and in c p less than group c versus group a total proteins albumin ALP phosphatase and fibronectin did not differ between groupsabstract truncated at words",
                "LOCATION": 89,
                "LABEL": "functional residual capacity"
            }
        },
    }
