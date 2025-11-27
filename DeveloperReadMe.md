<!-- DeveloperReadMe.md: Spring Boot -> FastAPI project mapping and developer onboarding -->

# Developer Guide — fast-api-project

This developer README is targeted at Spring Boot (Java) developers exploring a FastAPI (Python) project.
It walks through the Spring-like layout and explains how to extend it.

---

## Project structure (overview)

The project follows a layout inspired by Maven Spring Boot projects to make migration easier:

```
fast-api-project/
├── src/
│   ├── main/
│   │   ├── python/
│   │   │   └── app/
│   │   │       ├── controllers/     # Controllers: like Spring @Controller / @RestController
│   │   │       ├── services/        # Services: business logic (like @Service)
│   │   │       ├── repositories/    # Data access / DAO (like Spring Data Repos)
│   │   │       ├── models/          # Pydantic models (DTOs)
│   │   │       ├── config/          # App config (equivalent to application.yml)
│   │   │       └── main.py          # App bootstrap (like Spring Boot `main`)
│   │   └── resources/               # Static assets, templates
│   └── test/python/                 # Tests (pytest)
└── README.md                        # User-facing README with quick-start
    DeveloperReadMe.md               # Developer focused docs and extension instructions
```

### Spring Boot → FastAPI mapping

| Spring Boot (Maven) | FastAPI / Python (this repo)                                      |
| ------------------- | ----------------------------------------------------------------- |
| src/main/java       | src/main/python (Python package root for the app)                 |
| src/main/resources  | src/main/resources (static files)                                 |
| src/test/java       | src/test/python (pytest tests)                                    |
| Controller classes  | `app/controllers/` (APIRouter modules)                            |
| Service classes     | `app/services/` (business logic)                                  |
| Repository / DAO    | `app/repositories/` (DB clients and helpers)                      |
| Models / DTOs       | `app/models/` (Pydantic models for request/response schemas)      |
| Application config  | `app/config` (Python modules could read env vars or config files) |

---

## How to add a new controller (step-by-step)

1. Create a new module under `app/controllers`, e.g. `foo_controller.py`.

   - Start with `from fastapi import APIRouter` and create an `APIRouter` instance.
   - Add endpoints using decorators like `@router.get()` and provide `summary`, `description`, and `response_model`.

2. Register the controller: update `app/controllers/__init__.py` or add a new import there if you want the auto-registration.

   - `app.main` calls `get_routers()` which returns a list of routers. Add the router in `controllers.__init__` export.

3. Keep controllers thin: delegate complex logic to a `services` module.

   - Example: `from app.services.foo_service import create_foo`

4. If needed, add Pydantic models in `app/models` for request and response bodies.

5. Add tests under `src/test/python` for the new endpoint.

Example (controller snippet):

```python
from fastapi import APIRouter
from app.models.item import Item

router = APIRouter(tags=["Foo"])


@router.post("/foo", response_model=Item, summary="Create Foo", description="Creates a new Foo object")
async def create_foo(item: Item):
    # Call service layer
    return await some_service.create(item)
```

---

## How to add a new service (step-by-step)

1. Create a module under `app/services`, e.g. `foo_service.py`.
2. Implement the business logic in async functions (or sync if not interacting with DB).
3. Import the service in the controller and call functions from controllers.

Advantages of this layering:

- Testing: easier to test controllers and services in isolation.
- Responsibility: controllers only map HTTP ↔️ domain, services contain the business rules.

---

## OpenAPI Documentation (how endpoints are documented)

We use FastAPI’s OpenAPI generation. To maximize the `/docs` page:

- Provide `summary` and `description` in route decorators.
- Use `response_model` with Pydantic models to describe output shapes.
- Use `Field(..., description='...')` in models to document individual fields.
- Use `tags=["Tag Name"]` to group endpoints in the docs.

Example `@router.get` that produces rich docs:

```python
@router.get(
    "/items",
    response_model=list[Item],
    summary="Retrieve items",
    description="Returns up to the first 100 items from the configured collection",
    tags=["Items"],
)
async def get_items():
    ...
```

---

## Local developer tasks

- To run server (from project root):

```powershell
python -m pip install -r requirements.txt
python -m pip install -e .
python -m uvicorn app.main:app --reload --port 8005
```

- To run tests:

```powershell
.\venv\Scripts\pytest.exe -q
```

---

## Style and standards

- Keep endpoints small and use services for logic; controllers should only parse inputs and return results.
- Use Pydantic models for schemas and validation.
- Keep configuration in environment variables and avoid hard-coded secrets.

If you'd like, I can add a VS Code workspace configuration and a sample `Dockerfile` + `docker-compose.yml` for a Mongo + app dev environment.
