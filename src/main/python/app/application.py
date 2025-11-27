from pathlib import Path
import logging
from typing import Iterable

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRouter

from app.controllers import get_routers
from app.repositories import db as db_repo

logger = logging.getLogger("fastapi.app")
logging.basicConfig(level=logging.INFO)


class Application:
    """
    Application class that encapsulates FastAPI app creation, router registration,
    static mounting, and DB lifecycle management.

    This is the clear entry point class analogous to a Spring Boot Application class.
    """

    def __init__(self, title: str = "fast-api-project (Spring-style layout)", version: str = "0.1.0"):
        self.title = title
        self.version = version
        self.app = FastAPI(title=self.title, version=self.version)
        self._configure_static()
        self._register_routers()
        self._register_lifecycle_events()

    def _base_dir(self) -> Path:
        # points to src/main/python
        return Path(__file__).resolve().parents[2]

    def _configure_static(self) -> None:
        static_dir = self._base_dir() / "resources" / "static"
        if static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
            logger.info("Mounted static files from %s", static_dir)
        else:
            logger.warning("Static directory not found: %s", static_dir)

    def _register_routers(self) -> None:
        routers: Iterable[APIRouter] = get_routers()
        for r in routers:
            self.app.include_router(r)
        logger.info("Registered %d routers", len(list(routers)))

    def _register_lifecycle_events(self) -> None:
        @self.app.on_event("startup")
        async def _startup():
            logger.info("Application startup: initializing DB")
            await db_repo.init_db(self.app)

        @self.app.on_event("shutdown")
        async def _shutdown():
            logger.info("Application shutdown: closing DB")
            await db_repo.close_db(self.app)

    def get_app(self) -> FastAPI:
        return self.app

    def run(self, host: str = "0.0.0.0", port: int = 8000, reload: bool = True) -> None:
        import uvicorn

        uvicorn.run(self.app, host=host, port=port, reload=reload)