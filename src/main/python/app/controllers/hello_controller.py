from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse
from typing import Dict

router = APIRouter(prefix="", tags=["Hello"])


@router.get(
    "/",
    summary="Redirect to hello",
    description="Redirects the root path to `/hello`. This mirrors a Spring Boot `@GetMapping('/')` in controllers that route to a landing endpoint.",
)
async def root_redirect():
    """Redirect to `/hello`.

    Notes for a Spring developer: this is similar to a controller returning a `RedirectView` to route a base path.
    """
    return RedirectResponse(url="/hello")


@router.get(
    "/hello",
    summary="Hello endpoint",
    description="A basic 'Hello, World!' endpoint used for smoke tests and to confirm the application is responding.",
    response_model=Dict[str, str],
)
async def hello():
    """Return a simple JSON message for `/hello`.

    For a Spring user: this is the simplest controller method returning a response body. It uses FastAPI's
    native JSON encoding to create a response of the shape `{"message": "Hello, World!"}`.
    """
    return {"message": "Hello, World!"}


@router.get(
    "/favicon.ico",
    summary="Favicon",
    description="Returns the favicon used by the site (if present).",
    response_description="Binary favicon content",
)
async def favicon():
    """Return the static `favicon.ico` from resources.

    In Spring Boot you'd place static files under `src/main/resources/static`; we're doing the same here and mounting the folder in docs.
    """
    return FileResponse("src/main/resources/static/favicon.ico")
