# FastAPI + SQLAlchemy + Docker

This project provides a simple FastAPI application with SQLAlchemy and PostgreSQL, containerized with Docker Compose.

## Project Structure

```text
StateScan/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── __init__.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## How to Run the Application

### Option 1: Run with Docker Compose

From the project root, run:

```bash
docker compose up --build
```

This will start both the FastAPI app and the PostgreSQL database.

Once running, open:

- http://localhost:8000/health
- http://localhost:8000/items

### Option 2: Run Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
uvicorn app.main:app --reload
```

The app will be available at:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/items

### Stop the containers

```bash
docker compose down
```

## Example Requests

### Create an item

```bash
curl -X POST "http://localhost:8000/items" -H "Content-Type: application/json" -d '{"name":"sample item"}'
```

### List items

```bash
curl "http://localhost:8000/items"
```
