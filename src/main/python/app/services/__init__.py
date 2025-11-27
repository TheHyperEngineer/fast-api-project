from .item_service import ItemService

__all__ = ["ItemService", "item_service"]

# default instance for quick use in controllers
item_service = ItemService()