from epic_events.data.conf import session
from epic_events.models.models import Employee,Client, Event, Contract, Permission, Department


class EmployeeDao:
    def get_all(self):
        employees = session.query(Employee).all()
        return employees

    def get_by_id(employee_id):
        employee = session.query(Employee).get(employee_id)
        return employee

    def get_by_email(self, email: str):
        employee = session.query(Employee).filter(Employee.email == email).first()
        return employee

class ClientDao:
     def get_all(self):
        clients = session.query(Client).all()
        return clients

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


class ContractDao:
    def get_all(self):
        contract_all = session.query(Contract).all()
        return contract_all


class PermissionDao:
    def get_all(self):
        contract_all = session.query(Permission).all()
        return contract_all

    def get_by_id(self, permission_id):
        permission = session.query(Permission).get(permission_id)
        return permission
