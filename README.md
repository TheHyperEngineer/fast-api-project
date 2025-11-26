# Hello World — FastAPI + MongoDB demo

This repository contains a lightweight FastAPI application that demonstrates:

- Serving routes with FastAPI (GET /, /hello, /items, /db-info)
- Serving static files (mounted at `/static`)
- Connecting to MongoDB using Motor (async MongoDB driver)

---

## Quick start (Windows PowerShell)

1. Activate the sample virtualenv if you created one, or create a new venv and activate it:

```powershell
# If you already have the virtualenv in repo
.\hello-world-env\Scripts\Activate.ps1

# Or create one and activate:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install requirements:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Ensure MongoDB is running and accessible. If you run MongoDB in Docker (example):

```powershell
docker run -d -p 27017:27017 --name mongodb mongodb/mongodb-community-server
```

4. Start the app using uvicorn (from the project root):

```powershell
# Recommended: start uvicorn with module style so relative imports work as expected
python -m uvicorn main:app --host 127.0.0.1 --port 8005 --reload --log-level debug
```

> Important: Start `uvicorn` from the directory that contains `main.py`. Don’t run `python main.py` directly — using `-m uvicorn` loads the module correctly and enables reloader behavior.

---

## Environment variables

The project supports these env variables for Mongo configuration (defaults are set in `db.py`):

- `MONGO_URI` — MongoDB connection URI (default: `mongodb://localhost:27017`)
- `MONGO_DB` — MongoDB database name (default: `test`)
- `MONGO_COLLECTION` — MongoDB collection name (default: `medical`)

Example (PowerShell):

```powershell
$env:MONGO_URI = "mongodb://localhost:27017"
$env:MONGO_DB = "test"
$env:MONGO_COLLECTION = "your_collection"
python -m uvicorn main:app --reload --port 8005
```

---

## Basic endpoints

- GET `/hello` — returns `{"message":"Hello, World!"}`
- GET `/` — redirects to `/hello` (or you can return an HTML index or route to static)
- GET `/favicon.ico` — serves `static/favicon.ico` if present
- GET `/db-info` — returns diagnostics: available databases (list), collections for the configured DB, and a count for the configured collection
- GET `/items` — returns up to 100 documents from the configured `MONGO_COLLECTION` (ObjectIds are converted to strings)

Example curl calls:

```powershell
curl http://127.0.0.1:8005/hello
curl -i http://127.0.0.1:8005/db-info
curl -H "accept: application/json" http://127.0.0.1:8005/items
```

---

## Static files

- Static assets are served from `/static` via `app.mount('/static', StaticFiles(directory='static'))` in `main.py`.
- Create a `static` directory and add `favicon.ico` or `index.html` to avoid mount errors on startup:

```powershell
New-Item -ItemType Directory -Path .\static
# Add a favicon if you want
Invoke-WebRequest -Uri "https://www.google.com/favicon.ico" -OutFile .\static\favicon.ico
```

---

## Seeding data for quick testing

If you want to test `/items` you'll need documents in your Mongo collection. Using `mongosh` (in the running container or local install):

```powershell
# In a container named "mongodb" (example):
docker exec -it mongodb mongosh test --eval "db.your_collection.insertOne({name: 'hello', value: 1})"
```

Alternatively, seed with Python (`seed_db.py` sample)

```python
# seed_db.py
import asyncio
from db import collection

async def main():
    await collection.insert_one({"name": "test-item", "value": 123})

asyncio.run(main())
```

Run:

```powershell
python seed_db.py
```

---

## Troubleshooting

- `RuntimeError: Directory 'static' does not exist`

  - Create the `static` folder or conditionally mount it (`if os.path.isdir('static'):`) to avoid the startup failure.

- `ModuleNotFoundError: No module named 'db'` or `ImportError: attempted relative import with no known parent package`

  - Run uvicorn from the project root and use `python -m uvicorn main:app`, not `python main.py`.
  - Ensure `db.py` is in the project root and not in the `static` folder.

- `ObjectId is not JSON serializable`

  - The `GET /items` handler converts `_id` to string in the returned docs. If you have other unsupported BSON types, either serialize them (e.g., using `bson.json_util`) or map them to Python types.

- Port conflicts: If `Address already in use` errors appear, either free the port or run the server on another port.

---

## Git & cleaning up tracked files

- `.gitignore` is included to avoid committing virtualenvs, cache files, and sensitive `.env` files.
- If the virtualenv folder `hello-world-env` was committed previously, remove it from the repo cache (doesn’t delete it from disk):

```powershell
git rm -r --cached hello-world-env
git commit -m "Remove virtualenv; add .gitignore"
```

---

## Development tips

- Use `--reload` during development with uvicorn to auto-reload on code changes.
- Check logs for HTTP requests and errors in console output; `--log-level debug` shows more details.

---

If you want, I can:

- Add a `seed_db.py` file and a small test script for you, or
- Add a `Makefile` (or PowerShell script) to start the server, seed data, and run tests.

Tell me which action you’d like me to take next.
