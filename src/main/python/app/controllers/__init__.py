"""app.controllers package

This package exposes routers for the API which are included from `app.main`.
"""

from .hello_controller import router as hello_router
from .db_controller import router as db_router

__all__ = ["hello_router", "db_router"]


def get_routers():
    return [hello_router, db_router]
