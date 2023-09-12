from epic_events.data.conf import session
from epic_events.models.models import Employee, Event, Contract, Permission, Department

class EmployeeDao:
    def get_all(self):
        employees = session.query(Employee).all()
        return employees
    
    def get_by_id(employee_id):
        employee = session.query(Employee).get(employee_id)
        return employee
    
    def get_by_email(self, email:str):
        employee = session.query(Employee).filter(Employee.email==email).first()
        return employee
    
class DepartmentDao:
    def get_all(self):
        departments_all = session.query(Employee).all()
        return departments_all
    
    def get_by_id(department_id):
        department = session.query(Department).get(department_id)
        return department_id
