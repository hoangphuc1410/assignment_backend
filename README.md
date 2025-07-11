Backend Assignment FastAPI

This is a FastAPI microservice for an HR company. It powers the employee **search directory API**, supporting flexible filters like department, position, location, and employment status.

Features:
- FastAPI-based search API
- PostgreSQL + SQLAlchemy
- Rate-limiting
- Docker & Docker Compose support

Tech Stack:
- **FastAPI**: For building the API
- **SQLAlchemy**: For database interactions
- **Postgres**: As the database backend
- **Python 3.10+**: `httpx`, `pytest`, `passlib`, `pydantic`
- **Docker and Docker Compose setup**
- **Rate-limiting and dynamic** filtering support

Run via Docker
```bash
docker-compose up --build
```
