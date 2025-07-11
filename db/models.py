from enum import Enum as PyEnum # For creating the enum

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SqlEnum # For using in the table
from sqlalchemy.orm import relationship


class EmployeeStatus(str, PyEnum):
    active = "Active"
    not_started = "Not started"
    terminated = "Terminated"


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    contact_info = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")
    position_id = Column(Integer, ForeignKey("positions.id"))
    position = relationship("Position", back_populates="employees")
    location_id = Column(Integer, ForeignKey("locations.id"))
    location = relationship("Location", back_populates="employees")
    status = Column(SqlEnum(EmployeeStatus), default=EmployeeStatus.active)


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employees", back_populates="department")
    is_active = Column(Boolean, default=True)


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employees", back_populates="position")
    is_active = Column(Boolean, default=True)


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employees", back_populates="location")
    is_active = Column(Boolean, default=True)
