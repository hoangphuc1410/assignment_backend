from utils.rate_limiter import rate_limited
from enum import Enum

from typing import Annotated
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import Employees, Department, Location, Position

router = APIRouter(
    prefix="/employee",
    tags=["employee"],
)

db_dependency = Annotated[Session, Depends(get_db)]


class EmployeeStatus(str, Enum):
    active = "Active"
    not_started = "Not started"
    terminated = "Terminated"


class EmployeeTypeSearch(str, Enum):
    department = "Department"
    location = "Location"
    Position = "position"


@router.get("/search")
@rate_limited(max_calls=10, time_frame=60)  # Limit to 10 calls per minute
async def search_user(
        request: Request,
        employee_status: EmployeeStatus,
        employee_typ_search: EmployeeTypeSearch,
        db: db_dependency,
        query: str = Query("", description="Search query"),
        page: int = Query(1, ge=1),
        size: int = Query(50, le=100),
):
    base_query = db.query(Employees).join(Employees.department).join(Employees.position).join(Employees.location)
    # Filter by status
    base_query = base_query.filter(Employees.status == employee_status.value)

    # Filter by the selected search type
    if employee_typ_search == EmployeeTypeSearch.department:
        base_query = base_query.filter(Department.name.ilike(f"%{query}%"))
    elif employee_typ_search == EmployeeTypeSearch.location:
        base_query = base_query.filter(Location.name.ilike(f"%{query}%"))
    elif employee_typ_search == EmployeeTypeSearch.position:
        base_query = base_query.filter(Position.name.ilike(f"%{query}%"))

    # Pagination
    base_query = base_query.offset((page - 1) * size).limit(size)

    results = base_query.all()

    # Simple example output
    return {
        "results": [
            {
                "firstname": emp.firstname,
                "lastname": emp.lastname,
                "status": emp.status,
                "department": emp.department.name if emp.department else None,
                "position": emp.position.name if emp.position else None,
                "location": emp.location.name if emp.location else None,
            }
            for emp in results
        ],
        "page": page,
        "size": size
    }
