from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from db import client, database, collection
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root_redirect():
    return RedirectResponse(url="/hello")


@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")


@app.middleware("http")
async def log_path(request, call_next):
    print("REQUEST LOG:", request.method, request.url.path)
    return await call_next(request)


# main.py — add this route
@app.get("/db-info")
async def db_info():
    dbs = await client.list_database_names()
    collections = await database.list_collection_names()
    count = await collection.count_documents({})
    return {"databases": dbs, "collections": collections, "collection_count": count}


@app.get("/items")
async def read_items():
    try:
        items = await collection.find().to_list(100)
    except Exception as e:
        # DB error (e.g., connection issues) -> 500 with diagnostic
        raise HTTPException(status_code=500, detail=f"DB read failed: {e}")

    # Convert ObjectId to string for JSON serialization.
    for doc in items:
        if "_id" in doc:
            # cast ObjectId to string so the response is JSON serializable
            doc["_id"] = str(doc["_id"])

    if not items:
        return {"items": [], "warning": "collection is empty or wrong database/collection selected"}

    # If you want to ensure encoding for other types, use jsonable_encoder:
    # return jsonable_encoder(items)
    return items
