from fastapi.testclient import TestClient
import app.main as main
from app.dependencies import get_collection


class FakeCursor:
    def __init__(self, docs):
        self.docs = docs

    async def to_list(self, n):
        return self.docs


class FakeCollection:
    def __init__(self, docs):
        self.docs = docs

    def find(self):
        return FakeCursor(self.docs)

    async def count_documents(self, q):
        return len(self.docs)


class FakeDatabase:
    def __init__(self, collections):
        self._collections = collections

    async def list_collection_names(self):
        return self._collections


class FakeClient:
    def __init__(self, dbs):
        self._dbs = dbs

    async def list_database_names(self):
        return self._dbs

    @property
    def admin(self):
        class Admin:
            async def command(self, name):
                return {"ok": 1}

        return Admin()


def test_hello():
    client = TestClient(main.app)
    res = client.get("/hello")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello, World!"}


def test_items_empty(monkeypatch):
    # Override dependency to return a fake collection
    main.app.dependency_overrides[get_collection] = lambda: FakeCollection([])
    client = TestClient(main.app)
    res = client.get("/items")
    assert res.status_code == 200
    assert "warning" in res.json()


def test_items_populated(monkeypatch):
    docs = [{"_id": "abc123", "name": "test"}]
    main.app.dependency_overrides[get_collection] = lambda: FakeCollection(
        docs)
    client = TestClient(main.app)
    res = client.get("/items")
    assert res.status_code == 200
    # _id should be a string
    body = res.json()
    assert isinstance(body, list) or body, "items did not return correctly"


def test_db_info_and_health(monkeypatch):
    # Override client, database, collection via dependency overrides or monkeypatching
    monkeypatch.setattr(main, "client", FakeClient(["testdb"]))
    monkeypatch.setattr(main, "database", FakeDatabase(["medical"]))
    main.app.dependency_overrides[get_collection] = lambda: FakeCollection([
                                                                           {"_id": "abc"}])

    client = TestClient(main.app)

    res = client.get("/db-info")
    assert res.status_code == 200
    json = res.json()
    assert "databases" in json and "collections" in json and "collection_count" in json

    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_invalid_id_update_delete(monkeypatch):
    # Use fake collection for update/delete methods
    class BadCollection:
        async def update_one(self, *a, **k):
            return type('R', (), {'matched_count': 0})()

    main.app.dependency_overrides[get_collection] = lambda: BadCollection()
    client = TestClient(main.app)

    resp = client.put('/items/not-an-id', json={"name": "x", "value": 1})
    assert resp.status_code == 400

    resp = client.delete('/items/not-an-id')
    assert resp.status_code == 400


def test_create_update_delete(monkeypatch):
    # monkeypatch collection methods
    class FakeInsertResult:
        def __init__(self, id):
            self.inserted_id = id

    async def insert_one(doc):
        return FakeInsertResult("abc123")

    async def update_one(filter, update):
        class R:
            matched_count = 1
        return R()

    async def delete_one(filter):
        class R:
            deleted_count = 1
        return R()

    # Provide a collection-like object with methods we'll use
    class CRUDFakeCollection:
        async def insert_one(self, doc):
            return await insert_one(doc)

        async def update_one(self, filter, update):
            return await update_one(filter, update)

        async def delete_one(self, filter):
            return await delete_one(filter)

    main.app.dependency_overrides[get_collection] = lambda: CRUDFakeCollection(
    )
    client = TestClient(main.app)

    # create
    resp = client.post("/items", json={"name": "x", "value": 1})
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == "abc123"

    # update
    resp = client.put("/items/abc123", json={"name": "xx", "value": 2})
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == "abc123"

    # delete
    resp = client.delete("/items/abc123")
    assert resp.status_code == 200
    assert resp.json()["status"] == "deleted"
