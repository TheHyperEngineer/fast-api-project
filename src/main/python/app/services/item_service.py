from typing import List
from app.models.item import Item
from app.repositories.db import find_items

class ItemService:
    """
    Class-based service for item-related business logic.
    Instantiate this class in controllers or export a default instance.
    """

    async def get_items(self, limit: int = 100) -> List[Item]:
        docs = await find_items(limit=limit)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return [Item.model_validate(doc) for doc in docs]