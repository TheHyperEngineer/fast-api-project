import os
import logging
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from time import perf_counter

from .db import client, database
from .models import ItemIn, ItemOut
from .dependencies import get_collection, api_key_required

app = FastAPI()

# Prometheus metrics
REQUEST_COUNT = Counter('hello_requests_total', 'Total HTTP requests', [
                        'method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram(
    'hello_request_latency_seconds', 'Request latency seconds', ['endpoint'])

# Only mount static files if the directory exists to avoid startup errors
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Basic JSON logging config
# We'll set up a simple JSON logger (the Dockerfile/NGINX/Fluentd pipeline can pick this up)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    from pythonjsonlogger import jsonlogger

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.handlers = [logHandler]
except Exception:
    # python-json-logger missing; fallback to default logging
    pass


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
    logger.info("REQUEST LOG: %s %s", request.method, request.url.path)
    endpoint = request.url.path
    start = perf_counter()
    response = await call_next(request)
    duration = perf_counter() - start
    try:
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint,
                             http_status=response.status_code).inc()
    except Exception:
        # avoid failing the request if metrics fails
        pass
    return response


@app.get("/db-info")
async def db_info():
    dbs = await client.list_database_names()
    collections = await database.list_collection_names()
    count = await collection.count_documents({})
    return {"databases": dbs, "collections": collections, "collection_count": count}


@app.get("/items")
async def read_items(collection=Depends(get_collection)):
    try:
        items = await collection.find().to_list(100)
    except Exception as e:
        # DB error (e.g., connection issues) -> 500 with diagnostic
        raise HTTPException(status_code=500, detail=f"DB read failed: {e}")

    # Convert ObjectId to string for JSON serialization.
    for doc in items:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])

    if not items:
        return {"items": [], "warning": "collection is empty or wrong database/collection selected"}

    return items


@app.post("/items", response_model=ItemOut, dependencies=[Depends(api_key_required)])
async def create_item(item: ItemIn, collection=Depends(get_collection)):
    doc = item.dict()
    res = await collection.insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    # Map to the output model
    return {"id": doc["_id"], "name": doc["name"], "value": doc["value"]}


@app.put("/items/{item_id}", response_model=ItemOut, dependencies=[Depends(api_key_required)])
async def update_item(item_id: str, item: ItemIn, collection=Depends(get_collection)):
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    res = await collection.update_one({"_id": oid}, {"$set": item.dict()})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "name": item.name, "value": item.value}


@app.delete("/items/{item_id}", dependencies=[Depends(api_key_required)])
async def delete_item(item_id: str, collection=Depends(get_collection)):
    try:
        oid = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    res = await collection.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted"}


@app.get("/health")
async def health():
    """Health check: ping mongodb and return status."""
    try:
        await client.admin.command("ping")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB not ready: {e}")


@app.get('/metrics')
async def metrics():
    # Expose Prometheus metrics
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.on_event("startup")
async def on_startup():
    try:
        await client.admin.command("ping")
        logger.info("MongoDB reachable")
    except Exception as e:
        logger.warning("MongoDB is not reachable on startup: %s", e)


@app.on_event("shutdown")
async def on_shutdown():
    try:
        client.close()
        logger.info("MongoDB client closed")
    except Exception:
        pass
