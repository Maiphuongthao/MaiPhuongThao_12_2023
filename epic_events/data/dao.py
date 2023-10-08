import sentry_sdk
from sqlalchemy import select, update

from epic_events import errors
from epic_events.data.conf import session
from epic_events.models.models import (
    Client,
    Contract,
    Department,
    Employee,
    Event,
    Permission,
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
        if employee is None:
            raise errors.InvalidEmailError
        return employee

    def get_columns_key(self):
        return Employee.__table__.columns.keys()

    def add(self, datas):
        with sentry_sdk.start_transaction(op="task", name="Add employee"):
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

    @sentry_sdk.trace
    def update(self, key, value, employee):
        with sentry_sdk.start_transaction(op="task", name="Add employee"):
            if value:
                session.execute(
                    update(Employee),
                    [{"id": employee.id, key: value}],
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
        with sentry_sdk.start_transaction(op="task", name="Add client"):
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

    @sentry_sdk.trace
    def update(self, key, value, client):
        with sentry_sdk.start_transaction(op="task", name="Update client"):
            if value:
                session.execute(
                    update(Client),
                    [{"id": client.id, key: value}],
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
        event = session.query(Event).get(event_id)
        return event

    def get_columns_key(self):
        return Event.__table__.columns.keys()

    def add(self, datas):
        with sentry_sdk.start_transaction(op="task", name="Add event"):
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
        events = session.query(Event).filter(Event.support_id == support_id).all()
        return events

    def get_no_support(self):
        events = session.query(Event).filter(Event.support_id is None).all()
        return events

    @sentry_sdk.trace
    def update(self, key, value, event):
        with sentry_sdk.start_transaction(op="task", name="Update event"):
            if value:
                session.execute(
                    update(Event),
                    [{"id": event.id, key: value}],
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
        with sentry_sdk.start_transaction(op="task", name="Add contract"):
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
        contracts = session.query(Contract).filter(Contract.due_amount > 0).all()
        return contracts

    def get_unsigned_contracts(self):
        return session.query(Contract).filter(Contract.status == "en attend").all()

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

    @sentry_sdk.trace
    def update(self, key, value, contract):
        with sentry_sdk.start_transaction(op="task", name="Update contract"):
            if value:
                session.execute(
                    update(Contract),
                    [{"id": contract.id, key: value}],
                )
                session.commit()


class PermissionDao:
    def get_all(self):
        contract_all = session.query(Permission).all()
        return contract_all

    def get_by_id(self, permission_id):
        permission = session.query(Permission).get(permission_id)
        return permission
