from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from db.database import Base
from db.models import Base, Employees, Department, Position, Location, EmployeeStatus
from fastapi.testclient import TestClient
import pytest

from main import app


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1@localhost/AssignmentDatabase'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "phuc2984", "id": 1, "user_role": "admin"}  # Mock user for testing


client = TestClient(app)


@pytest.fixture
def test_search_employee():
    dept = Department(id=1, name="Engineering")
    pos = Position(id=1, name="Developer")
    loc = Location(id=1, name="Remote")
    emp = Employees(
        id=1,
        firstname="Alice",
        lastname="Smith",
        contact_info="alice@example.com",
        department=dept,
        position=pos,
        location=loc,
        status=EmployeeStatus.active,
    )
    db = TestingSessionLocal()
    db.add(emp)
    db.commit()
    yield emp
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM employees;"))
        connection.commit()
