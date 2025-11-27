"""app.services package

This package contains business logic (services) similar to `@Service` classes in a Spring Boot project.
Controllers should delegate application logic to services and keep their responsibilities small (HTTP concerns only).
"""

from .item_service import get_items

__all__ = ["get_items"]
