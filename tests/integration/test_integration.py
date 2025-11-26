import os
import subprocess
import time
import httpx
import pytest

COMPOSE_CMD = "docker compose"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture(scope="session")
def compose_up_and_teardown():
    # Run docker compose up
    subprocess.run(f"{COMPOSE_CMD} up --build -d",
                   shell=True, check=True, cwd=ROOT)

    # Wait for health endpoint
    for i in range(30):
        try:
            r = httpx.get("http://127.0.0.1:8005/health", timeout=2.0)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(1)
    else:
        # dump logs to help debug
        subprocess.run(f"{COMPOSE_CMD} logs",
                       shell=True, check=False, cwd=ROOT)
        subprocess.run(f"{COMPOSE_CMD} down --volumes --remove-orphans",
                       shell=True, check=False, cwd=ROOT)
        pytest.fail("Timed out waiting for app health check")

    yield

    # Teardown
    subprocess.run(f"{COMPOSE_CMD} down --volumes --remove-orphans",
                   shell=True, check=False, cwd=ROOT)


def test_health_and_dbinfo(compose_up_and_teardown):
    r = httpx.get("http://127.0.0.1:8005/health", timeout=5)
    assert r.status_code == 200
    j = r.json()
    assert j.get("status") == "ok"

    r = httpx.get("http://127.0.0.1:8005/db-info", timeout=5)
    assert r.status_code == 200
    j = r.json()
    assert "databases" in j
    assert "collections" in j


def test_seed_and_items(compose_up_and_teardown):
    # seed the DB using the provided script
    subprocess.run(f"{COMPOSE_CMD} run --rm app python seed_db.py",
                   shell=True, check=True, cwd=ROOT)

    r = httpx.get("http://127.0.0.1:8005/items", timeout=5)
    assert r.status_code == 200
    j = r.json()
    assert isinstance(j, list) or isinstance(j, dict)
    # Expect a non-empty list in either the 'items' key or the response body
    if isinstance(j, dict):
        assert j.get("items") is not None
    else:
        assert len(j) > 0


def test_crud_integration(compose_up_and_teardown):
    # create
    resp = httpx.post("http://127.0.0.1:8005/items",
                      json={"name": "it1", "value": 10}, timeout=5)
    assert resp.status_code == 200
    data = resp.json()
    item_id = data.get("id") or data.get("_id")
    assert item_id is not None

    # read
    resp = httpx.get("http://127.0.0.1:8005/items", timeout=5)
    assert resp.status_code == 200
    j = resp.json()
    # assert presence
    if isinstance(j, dict):
        # body-style
        assert any(x.get("_id") == item_id or x.get("id")
                   == item_id for x in j.get("items", []))
    else:
        assert any(x.get("_id") == item_id or x.get(
            "id") == item_id for x in j)

    # update
    resp = httpx.put(f"http://127.0.0.1:8005/items/{item_id}", json={
                     "name": "it1updated", "value": 20}, timeout=5)
    assert resp.status_code == 200
    j = resp.json()
    assert j["name"] == "it1updated"

    # delete
    resp = httpx.delete(f"http://127.0.0.1:8005/items/{item_id}", timeout=5)
    assert resp.status_code == 200
    assert resp.json().get("status") == "deleted"


def test_db_unavailable(compose_up_and_teardown):
    # Stop mongo service to simulate DB failure
    subprocess.run(f"{COMPOSE_CMD} stop mongodb",
                   shell=True, check=True, cwd=ROOT)
    try:
        r = httpx.get("http://127.0.0.1:8005/health", timeout=5)
        # app should respond with 503 if db is unreachable
        assert r.status_code == 503
    finally:
        subprocess.run(f"{COMPOSE_CMD} start mongodb",
                       shell=True, check=True, cwd=ROOT)
