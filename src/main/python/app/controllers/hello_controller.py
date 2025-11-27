from pathlib import Path
from typing import Dict

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse

class HelloController:
    """
    Class-based controller for hello endpoints.
    Exposes an APIRouter via the `router` property.
    """

    def __init__(self):
        self.router = APIRouter(prefix="", tags=["Hello"])
        self._register_routes()

    def _static_favicon_path(self) -> Path:
        # src/main/python -> parents[3] to reach src/main
        return Path(__file__).resolve().parents[3] / "resources" / "static" / "favicon.ico"

    def _register_routes(self):
        @self.router.get(
            "/",
            summary="Redirect to hello",
            description="Redirects the root path to `/hello`.",
        )
        async def root_redirect():
            return RedirectResponse(url="/hello")

        @self.router.get(
            "/hello",
            summary="Hello endpoint",
            description="A basic 'Hello, World!' endpoint used for smoke tests.",
            response_model=Dict[str, str],
        )
        async def hello():
            return {"message": "Hello, World!"}

        @self.router.get(
            "/favicon.ico",
            summary="Favicon",
            description="Returns the favicon used by the site (if present).",
        )
        async def favicon():
            p = self._static_favicon_path()
            if p.exists():
                return FileResponse(str(p))
            raise HTTPException(status_code=404, detail="favicon not found")