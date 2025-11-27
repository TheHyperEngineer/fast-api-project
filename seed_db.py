"""
Seed database helper

This simple script shows how to access the repository module (similar to a DAO in Spring) and insert a
sample document. Run it when the MongoDB server is available to seed a simple item for local testing.
"""

import asyncio
from app.repositories.db import collection


async def main():
    """Inserts a sample document into the configured collection."""
    await collection.insert_one({"name": "test-item", "value": 123})


if __name__ == "__main__":
    # Run seeding as a minimal script when executed from the project root
    asyncio.run(main())
