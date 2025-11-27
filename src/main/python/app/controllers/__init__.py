"""app.controllers package

This package exposes routers for the API which are included from `app.main`.
"""

from .hello_controller import router as hello_router
from .db_controller import router as db_router

__all__ = ["hello_router", "db_router"]


def get_routers():
    """Return a list of routers to include in the FastAPI app.

    This helps centralize controller registration; in a Spring Boot app, controllers are
    discovered and wired into the application context. Here, this function is the equivalent
    of collecting controller beans at startup and registering them on the router.
    """
    return [hello_router, db_router]
