from typing import List

from fastapi import APIRouter, HTTPException

from app.models.item import Item
from app.models.db_info import DBInfo
from app.services import item_service

from app.repositories import db as db_repo


class DBController:
    """
    Class-based controller for DB endpoints.
    """

    def __init__(self):
        self.router = APIRouter(prefix="", tags=["DB Endpoints"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get(
            "/db-info",
            response_model=DBInfo,
            summary="Database diagnostics",
            description="Returns available databases, collections in the configured DB, and a document count for the configured collection",
        )
        async def db_info():
            client = db_repo.get_client()
            database = db_repo.get_database()
            collection = db_repo.get_collection()

            if client is None or database is None or collection is None:
                raise HTTPException(status_code=503, detail="Database not initialized")

            dbs = await client.list_database_names()
            collections = await database.list_collection_names()
            count = await collection.count_documents({})
            return DBInfo(databases=dbs, collections=collections, collection_count=count)

        @self.router.get(
            "/items",
            response_model=List[Item],
            summary="Retrieve items",
            description="Returns up to the first 100 items from the configured Mongo collection; ObjectIds are converted to strings",
            responses={200: {"description": "List of items"}, 500: {"description": "Internal server error"}},
        )
        async def read_items():
            try:
                return await item_service.get_items(limit=100)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"DB read failed: {e}")