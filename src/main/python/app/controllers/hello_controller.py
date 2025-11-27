from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

router = APIRouter()


@router.get("/")
async def root_redirect():
    return RedirectResponse(url="/hello")


@router.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


@router.get("/favicon.ico")
async def favicon():
    return FileResponse("src/main/resources/static/favicon.ico")
