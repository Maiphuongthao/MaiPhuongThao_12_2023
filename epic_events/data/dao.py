from epic_events.data.conf import session
from sqlalchemy import select, update
from epic_events.models.models import (
    Employee,
    Client,
    Event,
    Contract,
    Permission,
    Department,
)


class EmployeeDao:
    def get_all(self):
        employees = session.query(Employee).all()
        return employees

    def get_by_id(self, employee_id):
        employee = session.query(Employee).get(employee_id)
        return employee

    def get_by_email(self, email: str):
        employee = session.query(Employee).filter(Employee.email == email).first()
        return employee

    def get_columns_key(self):
        return Employee.__table__.columns.keys()

    def add(self, datas):
        employee = Employee(
            name=datas["name"],
            email=datas["email"],
            password=datas["password"],
            department_id=datas["department_id"],
        )
        session.add(employee)
        session.commit()

    def delete(self, employee):
        session.delete(employee)
        session.commit()

    def update(self, key, value, employee):
        if value:
            #breakpoint()
            session.execute(
                update(Client),
                [{"id":employee.id, key: value}],
            )
            session.commit()
class ClientDao:
    def get_all(self):
        clients = session.query(Client).all()
        return clients

    def get_by_id(self, client_id):
        client = session.query(Client).get(client_id)
        return client

    def get_columns_key(self):
        return Client.__table__.columns.keys()

    def add(self, datas):
        client = Client(
            name=datas["name"],
            email=datas["email"],
            telephone=datas["telephone"],
            company_name=datas["company_name"],
            commercial_id=datas["commercial_id"],
        )
        session.add(client)
        session.commit()

    def get_by_commercial_id(self, commercial_id):
        clients = (
            session.execute(select(Client).where(Client.commercial_id == commercial_id))
            .scalars()
            .all()
        )
        return clients

    def update(self, key, value, client):
        if value:
            #breakpoint()
            session.execute(
                update(Client),
                [{"id":client.id, key: value}],
            )
            session.commit()


class DepartmentDao:
    def get_all(self):
        departments_all = session.query(Department).all()
        return departments_all

    def get_by_id(self, department_id):
        department = session.query(Department).get(department_id)
        return department


class EventDao:
    def get_all(self):
        events_all = session.query(Event).all()
        return events_all

    def get_by_id(self, event_id):
        event = session.query(Employee).get(event_id)
        return event

    def get_columns_key(self):
        return Event.__table__.columns.keys()

    def add(self, datas):
        event = Event(
            contract_id=datas["contract_id"],
            client_id=datas["client_id"],
            start_date=datas["start_date"],
            end_date=datas["end_date"],
            support_id=datas["support_id"],
            location=datas["location"],
            total_attendees=datas["total_attendees"],
            notes=datas["notes"],
        )
        session.add(event)
        session.commit()

    def get_by_support_id(self, support_id):
        events = (
            session.execute(select(Event).where(Event.support_id == support_id))
            .scalars()
            .all()
        )
        return events

    def get_no_support(self):
        events = session.execute(
            select(Event).where(
                Event.support_id == None,
            )
        ).scalars()
        return events
    
    def update(self, key, value, event):
        if value:
            #breakpoint()
            session.execute(
                update(Client),
                [{"id":event.id, key: value}],
            )
            session.commit()


class ContractDao:
    def get_all(self):
        contract_all = session.query(Contract).all()
        return contract_all

    def get_by_id(self, contract_id):
        contract = session.query(Contract).get(contract_id)
        return contract

    def get_columns_key(self):
        return Contract.__table__.columns.keys()

    def add(self, datas):
        contract = Contract(
            client_id=datas["client_id"],
            commercial_id=datas["commercial_id"],
            total_amount=datas["total_amount"],
            due_amount=datas["due_amount"],
            status=datas["status"],
        )
        session.add(contract)
        session.commit()

    def get_by_commercial_id(self, commercial_id):
        contracts = (
            session.execute(
                select(Contract).where(Contract.commercial_id == commercial_id)
            )
            .scalars()
            .all()
        )

        return contracts

    def get_due_amount_higher_than_zero(self):
        contracts = session.execute(
            select(Contract).where(
                Contract.due_amount > 0,
            )
        ).all()
        return contracts

    def get_unsigned_contracts(self):
        return (
            session.execute(
                select(Contract).filter_by(
                    status="en attend",
                )
            )
            .scalars()
            .all()
        )

    def get_signed_contract(self, employee_id):
        contracts = (
            session.execute(
                select(Contract)
                .where(Contract.commercial_id == employee_id)
                .where(Contract.status == "signé")
            )
            .scalars()
            .all()
        )
        return contracts

    def update(self, key, value, contract):
        if value:
            #breakpoint()
            session.execute(
                update(Client),
                [{"id":contract.id, key: value}],
            )
            session.commit()


class PermissionDao:
    def get_all(self):
        contract_all = session.query(Permission).all()
        return contract_all

    def get_by_id(self, permission_id):
        permission = session.query(Permission).get(permission_id)
        return permission
