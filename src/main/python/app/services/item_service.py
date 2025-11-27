"""
Item service layer.

Purpose:
- In Spring Boot, this would be a `@Service` class containing business logic and orchestration.
- We provide a thin service layer so `controllers` don't access the DB directly—this helps keep
  controllers focused on web concerns and makes the app easier to test.
"""
from typing import List
from app.models.item import Item
from app.repositories.db import collection


async def get_items(limit: int = 100) -> List[Item]:
    """Retrieve items (via repository) and convert to validated Item models.

    Args:
        limit: number of documents to return

    Returns:
        List[Item]: a list of Pydantic models representing collection documents
    """
    docs = await collection.find().to_list(limit)
    # Convert ObjectId `_id` to string; Item will validate schema
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    # Compute typed conversion using Item model
    return [Item.model_validate(doc) for doc in docs]
