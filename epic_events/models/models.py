import datetime
from typing import List

from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from epic_events.data.conf import Base


class Employee(Base):
    #table employees
    __tablename__ = 'employees'
    #columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    clients: Mapped[List['Client']] = relationship(back_populates='commercial')
    events: Mapped[List['Event']] = relationship(back_populates='support')
    department: Mapped['Department'] = relationship(back_populates='employees')
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    
class Department(Base):
    __tablename__='departments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    employees: Mapped[List['Employee']] = relationship(back_populates='department')

class Client(Base):
    #table clients
    __tablename__='clients'
    #columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    telephone: Mapped[str] = mapped_column(String(20))
    company_name: Mapped[str] = mapped_column(String(100))
    events: Mapped[List['Event']] = relationship(back_populates='client')
    contracts: Mapped[List['Contract']] = relationship(back_populates='client')                                             
    commercial: Mapped[List['Employee']] = relationship(back_populates='clients')
    commercial_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    created_date: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    last_update: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())

class Contract(Base):
    __tablename__='contracts'

    id: Mapped[int] = mapped_column(primary_key=True)
    client: Mapped['Client'] = relationship(back_populates='contracts')
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    total_amount: Mapped[float] = mapped_column(Float)
    due_amount: Mapped[float] = mapped_column(Float)                       
    commercial: Mapped['Employee'] = relationship(back_populates='contracts')
    commercial_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    created_date: Mapped[datetime.datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    status: Mapped[str] = mapped_column(String(30))  
    events: Mapped[List['Event']] = relationship(back_populates='contract')

class Event(Base):
    __tablename__='events'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    contract: Mapped['Client'] = relationship(back_populates='events')
    contract_id: Mapped[int] = mapped_column(ForeignKey('contracts.id'))
    client: Mapped['Client'] = relationship(back_populates='events')
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    start_date: Mapped[str]=mapped_column(String(30))
    end_date: Mapped[str]=mapped_column(String(30))                                            
    support: Mapped['Employee'] = relationship(back_populates='events')
    support_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    location: Mapped[str]=mapped_column(String(150))
    total_attendees: Mapped[int]=mapped_column(Integer)
    note: Mapped[str]=mapped_column(String(1024), nullable=True)


