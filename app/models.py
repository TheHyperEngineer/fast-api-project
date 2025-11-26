from pydantic import BaseModel
from typing import Optional


class ItemIn(BaseModel):
    name: str
    value: int


class ItemOut(ItemIn):
    id: Optional[str]
