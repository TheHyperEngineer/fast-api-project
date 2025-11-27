"""
Controller package initializer.

This module instantiates controller classes and returns their routers via get_routers().
"""

from .hello_controller import HelloController
from .db_controller import DBController

__all__ = ["get_routers"]


def get_routers():
    """
    Instantiate controllers and return a list of APIRouter instances to be included
    in the FastAPI app.
    """
    controllers = [
        HelloController(),
        DBController(),
    ]
    return [c.router for c in controllers]