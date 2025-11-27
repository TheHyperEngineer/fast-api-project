from fastapi import APIRouter, HTTPException
from app.repositories.db import client, database
from app.services.item_service import get_items
from app.models.item import Item
from app.models.db_info import DBInfo

router = APIRouter(prefix="", tags=["DB Endpoints"])


@router.get(
    "/db-info",
    response_model=DBInfo,
    summary="Database diagnostics",
    description="Returns available databases, collections in the configured DB, and a document count for the configured collection",
)
async def db_info():
    dbs = await client.list_database_names()
    collections = await database.list_collection_names()
    # keep collection count logic local to repo or service; we get the collection configured in repo
    count = 0
    from app.repositories.db import collection

    count = await collection.count_documents({})
    return DBInfo(databases=dbs, collections=collections, collection_count=count)


@router.get(
    "/items",
    response_model=list[Item],
    summary="Retrieve items",
    description="Returns up to the first 100 items from the configured Mongo collection; ObjectIds are converted to strings",
    responses={
        200: {"description": "List of items"},
        500: {"description": "Internal server error"},
    },
)
async def read_items():
    try:
        return await get_items(limit=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB read failed: {e}")
