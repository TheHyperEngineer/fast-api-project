from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.controllers import get_routers

app = FastAPI()
app.mount(
    "/static", StaticFiles(directory="src/main/resources/static"), name="static")

# Include routers from controllers package
for r in get_routers():
    app.include_router(r)


# Root and static endpoints are defined in controllers/hello_controller.py


@app.middleware("http")
async def log_path(request, call_next):
    print("REQUEST LOG:", request.method, request.url.path)
    return await call_next(request)


# DB endpoints are defined in controllers/db_controller.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
