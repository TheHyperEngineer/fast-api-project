from fastapi import APIRouter, HTTPException
from app.repositories.db import client, database, collection

router = APIRouter()


@router.get("/db-info")
async def db_info():
    dbs = await client.list_database_names()
    collections = await database.list_collection_names()
    count = await collection.count_documents({})
    return {"databases": dbs, "collections": collections, "collection_count": count}


@router.get("/items")
async def read_items():
    try:
        items = await collection.find().to_list(100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB read failed: {e}")

    for doc in items:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])

    if not items:
        return {"items": [], "warning": "collection is empty or wrong database/collection selected"}

    return items
