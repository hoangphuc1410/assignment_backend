from fastapi import status

from db.database import get_db
from .utils import *

app.dependency_overrides[get_db] = override_get_db


def test_return_user():
    response = client.get(
        "/employee/search",
        params={
            "employee_status": "Active",
            "employee_typ_search": "Department",
            "query": "Engineer",
            "page": 1,
            "size": 10
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["firstname"] == "Alice"
