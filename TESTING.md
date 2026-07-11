# Testing Guide

This guide explains how to test the FastAPI application with `pytest`. It is intended to help new developers understand the test strategy, where tests live, which scenarios should be covered, and how to run the suite locally or in Docker.

## Objectives

The test suite verifies that the application behaves correctly at the API, validation, and database layers. All automated tests should be written with `pytest` and should be easy to run without manual setup.

The testing strategy is to:

- Exercise public FastAPI endpoints through `fastapi.testclient.TestClient`.
- Use a dedicated test database, such as SQLite or another isolated database, instead of production data.
- Verify database persistence directly for create, update, and delete operations.
- Cover successful paths, validation failures, and error handling paths.
- Keep tests independent, repeatable, and readable.

## Test Directory Structure

Tests should be organized in a dedicated `tests/` directory. Separate files by application behavior or component so that the suite remains maintainable as the project grows.

Recommended structure:

```text
tests/
├── __init__.py
├── conftest.py
├── test_health.py
├── test_items_crud.py
├── test_items_validation.py
├── test_items_not_found.py
└── test_database.py
```

Recommended responsibilities:

- `conftest.py`: shared fixtures, test database setup, dependency overrides, reusable API clients, and sample payloads.
- `test_health.py`: health endpoint tests.
- `test_items_crud.py`: item create, read, update, and delete endpoint tests.
- `test_items_validation.py`: request payload validation tests.
- `test_items_not_found.py`: error handling for missing item resources.
- `test_database.py`: direct database connection and persistence tests.

## Test Scenarios

### Health Check

Health endpoint tests should verify that:

- The application health endpoint returns a successful HTTP response.
- The response status code is `200`.
- The response payload matches the expected health response, such as `{"status": "ok"}`.

### Create (POST)

Create endpoint tests should verify that:

- A new item can be created successfully with valid data.
- The response contains the newly created item data.
- The response includes an item identifier.
- Returned fields match the submitted values.
- The created record is persisted in the test database.

### Read (GET)

Read endpoint tests should verify that:

- All item records can be retrieved from `GET /items`.
- A single item can be retrieved by ID from `GET /items/{item_id}`.
- Response payloads include the expected fields and structure.
- Returned data matches the records stored in the database.

### Update (PUT/PATCH)

Update endpoint tests should verify that:

- An existing item can be updated successfully.
- Updated values are returned in the API response.
- Fields not included in a partial update remain unchanged, if partial updates are supported.
- Updated values are persisted in the database.

The current API supports updates with `PUT /items/{item_id}`. If a `PATCH /items/{item_id}` endpoint is added in the future, it should have equivalent test coverage for partial update behavior.

### Delete (DELETE)

Delete endpoint tests should verify that:

- An existing item can be deleted successfully.
- The API returns the expected success response.
- The deleted record no longer exists in the database.
- Fetching the deleted record returns the expected not-found response.

## Request Validation

Request validation tests should cover invalid or malformed input and verify that FastAPI/Pydantic returns the correct HTTP status code and validation response.

Include test cases for:

- Missing required fields, such as `name` or `price` when creating an item.
- Empty values, such as an empty string for `name`.
- Invalid data types, such as a non-numeric value for `price`.
- Invalid numeric values, such as `0` or negative prices when `price` must be greater than `0`.
- Invalid request payloads, such as malformed JSON.
- Additional unexpected fields, if the schemas are configured to reject extra fields.

Expected validation behavior:

- Invalid create or update requests should return `422 Unprocessable Entity`.
- The response body should include a `detail` field describing validation failures.
- Tests should assert both the status code and the presence of validation details.

## Error Handling

Error handling tests should verify consistent API behavior for invalid resource operations.

Include test cases for:

- Retrieving a non-existent record with `GET /items/{item_id}`.
- Updating a non-existent record with `PUT /items/{item_id}`.
- Deleting a non-existent record with `DELETE /items/{item_id}`.
- Invalid endpoint requests, if applicable.

Expected error behavior:

- Missing item resources should return `404 Not Found`.
- The response body should include a clear error message, such as `{"detail": "Item not found"}`.
- Tests should assert both status codes and response payloads.

## Database Testing

Database tests should prove that the persistence layer works without risking production data.

Guidelines:

- Use the dedicated PostgreSQL test database configured with `TEST_DB_*`; do not silently fall back to an in-memory database.
- Never run automated tests against production data.
- Override the application database dependency during tests so API calls use the test database.
- Create database tables before each test or test session as appropriate.
- Clean up test data after each test so tests remain independent.
- Keep tests repeatable and avoid relying on execution order.
- Verify create, read, update, and delete behavior directly through SQLAlchemy sessions where useful.

A typical pytest setup uses `tests/conftest.py` to define:

- A test database URL.
- A SQLAlchemy test engine and session factory.
- A `get_db` dependency override for FastAPI.
- A `TestClient` fixture.
- Setup and teardown fixtures that create and drop tables.


## Test Database Configuration

The application builds its database connection from environment variables. A standalone PostgreSQL Docker container must be running before tests start, and `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` must point to that container.

The pytest suite requires a separate `TEST_DB_HOST`, `TEST_DB_PORT`, `TEST_DB_NAME`, `TEST_DB_USER`, and `TEST_DB_PASSWORD` configuration. Test startup fails if any required test database variable is missing, if SQLAlchemy cannot create a connection, or if the active database name does not match `TEST_DB_NAME`. The test setup copies the explicit `TEST_DB_*` values into the application `DB_*` variables before importing the FastAPI app so API tests exercise the app against the dedicated test database instead of the application database.

## Running the Tests

### Install Test Dependencies

Install the application and test dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

The test suite requires `pytest` and `httpx` in addition to the FastAPI application dependencies.

### Run All Tests

Run the full suite:

```bash
pytest
```

### Run Tests with Verbose Output

Run the full suite with detailed output:

```bash
pytest -v
```

### Run an Individual Test File

Run one test module:

```bash
pytest tests/test_items_crud.py -v
```

Other useful examples:

```bash
pytest tests/test_health.py -v
pytest tests/test_items_validation.py -v
pytest tests/test_items_not_found.py -v
pytest tests/test_database.py -v
```


### External Docker API Checks

Automated pytest tests in this repository use `fastapi.testclient.TestClient`, so they run directly against the FastAPI app instance and do not require a localhost port. If you add external integration tests or manual checks that call the running Docker Compose service, use the host-mapped Docker URL:

```text
http://<your-machine-ip>:9000
```

Useful Docker Compose verification URLs:

```text
http://<your-machine-ip>:9000/health
http://<your-machine-ip>:9000/items
http://<your-machine-ip>:9000/docs
```

### Run Tests Inside Docker

Docker Compose automatically executes the full test suite before starting FastAPI:

```bash
docker compose up --build
```

During startup, the `web` container validates the connection to the already-running standalone PostgreSQL container, runs `pytest -v tests`, prints pytest progress and the final summary to the container logs, and starts Uvicorn only when every test passes. If the database connection fails or any test fails, Docker startup stops before the API server is launched.

For this repository, the application service is named `web`. To rerun tests manually in an already running container, use:

```bash
docker compose exec web pytest -v tests
```

If your Docker Compose service is named differently, replace `web` with the correct service name.

## Expected Outcome

A healthy test suite should meet these expectations:

- All tests pass successfully.
- Tests can be run repeatedly without manual cleanup.
- Tests are independent and do not depend on execution order.
- Tests do not modify production data.
- Tests follow pytest best practices, including clear fixture usage and readable assertions.
- Test reports clearly show which application behavior passed or failed.
- New developers can follow this guide to install dependencies, understand test coverage, and run the suite confidently.
