import asyncio
from app.db import collection


async def main():
    # Insert a few sample documents
    docs = [
        {"name": "test-item-1", "value": 1},
        {"name": "test-item-2", "value": 2}
    ]
    await collection.insert_many(docs)
    print("Inserted sample documents")

if __name__ == '__main__':
    asyncio.run(main())
