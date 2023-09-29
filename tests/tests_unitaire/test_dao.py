from epic_events.data.dao import EmployeeDao, ClientDao, ContractDao, PermissionDao, EventDao
from epic_events.models import models
from sqlalchemy import select
import pytest

ed = EmployeeDao()
cd = ClientDao()
ctd = ContractDao()
pd = PermissionDao()
evd = EventDao()


@pytest.fixture
def client2(connection):
    client2 = models.Client(
        name="Client2",
        email="client2@test.com",
        telephone="0124578",
        company_name="company_1",
        commercial_id=1,
    )
    connection.add(client2)
    connection.commit()
    return client2

# @pytest.fixture
# def contract2(connection):
#     contract2 = models.Contract(
#         client_id=client2.id,
#         commercial_id=1,
#         total_amount=100.00,
#         due_amount=20.00,
#         status="signée",
#     )
#     connection.add(contract2)
#     connection.commit()
#     return contract2

# @pytest.fixture
# def event2(connection):
#     event2 = models.Event(
#         contract_id=1,
#         client_id=1,
#         start_date="01/01/2024",
#         end_date="01/10/2024",
#         support_id=3,
#         location="Paris",
#         total_attendees=20,
#         notes=None,
#     )
#     connection.add(event2)
#     connection.commit()
#     return event2

class TestEmployeeDao:
    def test_get_all_employee(self, monkeypatch, connection):
        employees = connection.query(models.Employee).all()
        session = connection.query(models.Employee)
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Employee: session
        )
        assert ed.get_all() == employees

    def test_employee_get_by_id(self, connection, dummy_employee_gestion, monkeypatch):
        employee = connection.query(models.Employee).get(dummy_employee_gestion.id)
        session = connection.query(models.Employee)
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Employee: session
        )
        assert ed.get_by_id(dummy_employee_gestion.id) == employee

    def test_get_by_email(self, connection, dummy_employee_gestion, monkeypatch):
        employee = (
            connection.query(models.Employee)
            .filter(models.Employee.email == dummy_employee_gestion.email)
            .first()
        )
        session = connection.query(models.Employee)
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Employee: session
        )
        assert ed.get_by_email(dummy_employee_gestion.email) == employee


class TestClientDao:
    def test_get_all_client(self, monkeypatch, connection, dummy_employee_commercial):
        session = connection.query(models.Client)
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Client: session
        )
        assert cd.get_all() == connection.query(models.Client).all()

    def test_client_get_by_id(self, connection, client2, monkeypatch):
        client = connection.query(models.Client).get(1)

        session = connection.query(models.Client)
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Employee: session
        )
        result = ed.get_by_id(1)
        assert result == client


class TestContractDao:
    def test_signed_contract(self, connection, dummy_employee_commercial, monkeypatch):
        session = connection.execute(select(models.Contract))
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Contract: session
        )
        commercial_id = dummy_employee_commercial.id
        contracts = (
            connection.query(models.Contract)
            .filter(
                models.Contract.commercial_id == dummy_employee_commercial.id,
                models.Contract.status == "signée",
            )
            .all()
        )
        result = ctd.get_signed_contract(commercial_id)

        assert result == contracts

    def test_contract_by_commercial_id(self, connection, dummy_employee_commercial, monkeypatch):
        session = connection.execute(select(models.Contract))
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Contract: session
        )
        commercial_id = dummy_employee_commercial.id
        contracts = (
            connection.query(models.Contract)
            .filter(
                models.Contract.commercial_id == dummy_employee_commercial.id,
                models.Contract.status == "signée",
            )
            .all()
        )
        result = ctd.get_by_commercial_id(commercial_id)

        assert result == contracts

    def test_add_contract(self, connection, monkeypatch):
        datas = {"client_id":1,
        "commercial_id":1,
        "total_amount":100.00,
        "due_amount":20.00,
        "status":"signée",}

        
        monkeypatch.setattr(
            "epic_events.data.dao.session.add", lambda Contract: connection
        )
        result = ctd.add(datas)

        assert result == connection.query(models.Contract).filter(models.Contract.id == 1).first()

class TestPermissionDao:
    def test_permissions_get_all(self, connection, monkeypatch):
        session = connection.query(models.Permission)
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Permission: session
        )
        assert pd.get_all() == connection.query(models.Permission).all()

    def test_permission_get_by_id(self, connection, monkeypatch):
        client = connection.query(models.Permission).get(1)

        session = connection.query(models.Permission)
        monkeypatch.setattr(
            "epic_events.data.dao.session.query", lambda Permission: session
        )
        result = pd.get_by_id(1)
        assert result == client

