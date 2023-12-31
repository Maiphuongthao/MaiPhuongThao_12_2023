import datetime
from typing import List

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from epic_events.data.conf import Base


class Employee(Base):
    # table employees
    __tablename__ = "employees"
    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped["Department"] = relationship(back_populates="employees")
    clients: Mapped[List["Client"]] = relationship(back_populates="commercial")
    events: Mapped[List["Event"]] = relationship(back_populates="support")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="commercial")


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    employees: Mapped[List["Employee"]] = relationship(back_populates="department")
    permissions: Mapped[List["Permission"]] = relationship(back_populates="department")


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    department: Mapped["Department"] = relationship(back_populates="permissions")
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    ob_name: Mapped[str] = mapped_column(String(50))
    ob_action: Mapped[str] = mapped_column(String(50))
    ob_type: Mapped[str] = mapped_column(String(50))
    ob_field: Mapped[str] = mapped_column(String(200))


class Client(Base):
    # table clients
    __tablename__ = "clients"
    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    telephone: Mapped[str] = mapped_column(String(20))
    company_name: Mapped[str] = mapped_column(String(100))
    events: Mapped[List["Event"]] = relationship(back_populates="client")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="client")
    commercial: Mapped["Employee"] = relationship(back_populates="clients")
    commercial_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_update: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Contract(Base):
    __tablename__ = "contracts"
    id: Mapped[int] = mapped_column(primary_key=True)
    client: Mapped["Client"] = relationship(back_populates="contracts")
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    commercial: Mapped["Employee"] = relationship(back_populates="contracts")
    commercial_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=True)
    total_amount: Mapped[float] = mapped_column(Float)
    due_amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30))
    events: Mapped[List["Event"]] = relationship(back_populates="contract")
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract: Mapped["Contract"] = relationship(back_populates="events")
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    client: Mapped["Client"] = relationship(back_populates="events")
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    start_date: Mapped[str] = mapped_column(String(30))
    end_date: Mapped[str] = mapped_column(String(30))
    support: Mapped["Employee"] = relationship(back_populates="events")
    support_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=True)
    location: Mapped[str] = mapped_column(String(150))
    total_attendees: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(String(1024), nullable=True)
