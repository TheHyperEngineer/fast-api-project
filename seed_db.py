import asyncio
from app.repositories.db import collection


async def main():
    await collection.insert_one({"name": "test-item", "value": 123})

if __name__ == "__main__":
    asyncio.run(main())
