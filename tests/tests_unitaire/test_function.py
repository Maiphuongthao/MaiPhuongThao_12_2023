from epic_events.controller.login_controller import MenuController
from epic_events.models import models


def test_read(dummy_employee_gestion, monkeypatch):
    mc = MenuController()
    monkeypatch.setattr(
        "epic_events.controller.login_controller.MenuController.get_ob_by_id",
        lambda self, prompt: dummy_employee_gestion,
    )
    mc.read_one("employee", dummy_employee_gestion)
    assert "employee id :2"


def test_read_client_contract_event(
    connection, dummy_employee_support, dummy_employee_commercial, monkeypatch, capsys
):
    client1 = models.Client(
        name="Client1",
        email="client1@test.com",
        telephone="0124578",
        company_name="company_1",
        commercial_id=dummy_employee_commercial.id,
    )
    connection.add(client1)
    connection.commit()
    contract1 = models.Contract(
        client_id=client1.id,
        commercial_id=dummy_employee_commercial.id,
        total_amount=200.00,
        due_amount=10.00,
        status="en attend",
    )
    connection.add(contract1)
    connection.commit()
    event1 = models.Event(
        contract_id=contract1.id,
        client_id=client1.id,
        start_date="01/01/2024",
        end_date="01/10/2024",
        support_id=dummy_employee_support.id,
        location="Paris",
        total_attendees=20,
        notes=None,
    )
    connection.add(event1)
    connection.commit()

    mc = MenuController()
    monkeypatch.setattr(
        "epic_events.controller.login_controller.MenuController.get_ob_by_id",
        lambda self, prompt: client1,
    )
    mc.read_one("client", client1)
    assert "client id :2" in capsys.readouterr().out

    monkeypatch.setattr(
        "epic_events.controller.login_controller.MenuController.get_ob_by_id",
        lambda self, prompt: contract1,
    )
    mc.read_one("contract", contract1)
    assert "contract id :1" in capsys.readouterr().out

    monkeypatch.setattr(
        "epic_events.controller.login_controller.MenuController.get_ob_by_id",
        lambda self, prompt: event1,
    )
    mc.read_one("event", event1)
    assert "event id :1" in capsys.readouterr().out


def test_read_all_employee(connection, capsys):
    mc = MenuController()
    mc.read_all("employee")

    captured_stdout = capsys.readouterr().out
    assert "Liste des employees" in captured_stdout


def test_read_all_event(connection, capsys):
    mc = MenuController()
    mc.read_all("event")

    captured_stdout = capsys.readouterr().out
    assert "Liste des events" in captured_stdout


def test_create_employee(monkeypatch, connection, capsys, dummy_employee_gestion):
    mc = MenuController()
    datas = {
        "name": "gestion2",
        "email": "gestion2@test.com",
        "password": "Pasword12@",
        "department_id": 2,
    }

    monkeypatch.setattr(
        "epic_events.view.view.MenuView.propmt_for_data_creation",
        lambda x, y, z: datas,
    )
    monkeypatch.setattr(
        "epic_events.controller.login_controller.get_user_id",
        lambda: dummy_employee_gestion.id,
    )
    monkeypatch.setattr(
        "epic_events.data.dao.session.add",
        lambda x: connection,
    )

    mc.create_one("employee")
    assert "Nouveau employée a été crée." in capsys.readouterr().out


def test_update_employee(monkeypatch, connection, capsys, dummy_employee_gestion):
    mc = MenuController()

    value = ["name", "gestion_1"]
    fields = ["name", "email", "password", "department_id"]
    monkeypatch.setattr(
        "epic_events.view.view.MenuView.prompt_for_update",
        lambda x, y, z, prompt: value,
    )
    monkeypatch.setattr(
        "epic_events.controller.login_controller.get_user_id",
        lambda: dummy_employee_gestion.id,
    )
    monkeypatch.setattr(
        "epic_events.controller.login_controller.ob_field_for_update",
        lambda x, y: fields,
    )
    monkeypatch.setattr(
        "epic_events.data.dao.session.execute",
        lambda x, id: connection,
    )

    mc.update("employee", dummy_employee_gestion)
    assert "employée a été modifié" in capsys.readouterr().out


def test_delete(monkeypatch, connection, capsys, dummy_employee_gestion):
    mc = MenuController()
    monkeypatch.setattr(
        "epic_events.controller.login_controller.MenuController.get_ob_by_id",
        lambda self, ob_name, delete: dummy_employee_gestion,
    )
    monkeypatch.setattr(
        "epic_events.data.dao.session.delete",
        lambda x: connection,
    )
    mc.delete("employee")
    assert "employée a été supprimé" in capsys.readouterr().out


def test_read_no_support(monkeypatch, connection, capsys):
    mc = MenuController()
    liste = connection.query(models.Event).filter(models.Event.support_id is None).all()
    monkeypatch.setattr(
        "epic_events.data.dao.session.query",
        lambda x, id: connection,
    )
    monkeypatch.setattr("epic_events.data.dao.EventDao.get_no_support", lambda _: liste)
    mc.read_no_support("event")
    assert "Liste des events" in capsys.readouterr().out


def test_read_no_signature(monkeypatch, connection, capsys):
    mc = MenuController()
    liste = (
        connection.query(models.Contract)
        .filter(models.Contract.status == "en attend")
        .all()
    )
    monkeypatch.setattr(
        "epic_events.data.dao.session.query",
        lambda x, id: connection,
    )
    monkeypatch.setattr(
        "epic_events.data.dao.ContractDao.get_unsigned_contracts", lambda _: liste
    )
    mc.read_no_signature("contract")
    assert "Liste des contracts" in capsys.readouterr().out


def test_read_due_amount(monkeypatch, connection, capsys):
    mc = MenuController()
    liste = (
        connection.query(models.Contract).filter(models.Contract.due_amount > 0).all()
    )
    monkeypatch.setattr(
        "epic_events.data.dao.session.query",
        lambda x, id: connection,
    )
    monkeypatch.setattr(
        "epic_events.data.dao.ContractDao.get_due_amount_higher_than_zero",
        lambda _: liste,
    )
    mc.read_due_amount("contract")
    assert "Liste des contracts" in capsys.readouterr().out


def test_read_owned(monkeypatch, dummy_employee_support, connection, capsys):
    mc = MenuController()
    liste = (
        connection.query(models.Event)
        .filter(models.Event.support_id == dummy_employee_support.id)
        .all()
    )
    monkeypatch.setattr(
        "epic_events.data.dao.session.query",
        lambda x, id: connection,
    )
    monkeypatch.setattr(
        "epic_events.data.dao.EventDao.get_by_support_id",
        lambda self, employee_id: liste,
    )
    monkeypatch.setattr(
        "epic_events.controller.login_controller.get_user_id",
        lambda: dummy_employee_support.id,
    )
    mc.read_owned("event")
    assert "Liste des events" in capsys.readouterr().out


def test_get_ob_by_id(monkeypatch, dummy_employee_support, connection):
    mc = MenuController()
    monkeypatch.setattr(
        "epic_events.controller.login_controller.get_user_id",
        lambda: dummy_employee_support.id,
    )
    ob_name = "employee"
    action = "read"
    session = connection.query(models.Employee)
    monkeypatch.setattr("epic_events.data.dao.session.query", lambda Employee: session)
    monkeypatch.setattr(
        "epic_events.data.dao.EmployeeDao.get_by_id",
        lambda self, id: dummy_employee_support.id,
    )
    monkeypatch.setattr(
        "epic_events.view.view.MenuView.prompt_for_object_id",
        lambda self, ob, act, id: dummy_employee_support.id,
    )

    result = mc.get_ob_by_id(ob_name, action)

    assert result == 3
