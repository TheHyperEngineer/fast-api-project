"""app.models package

This package contains Pydantic models used for validation and OpenAPI documentation. Models are
analogous to DTOs or domain objects in Spring Boot that are used for binding and validation.
"""

from .item import Item
from .db_info import DBInfo

__all__ = ["Item", "DBInfo"]
