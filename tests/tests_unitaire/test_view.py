from epic_events.models import models
from epic_events.view.view import MenuView, LoginView
from epic_events.view import view
import pytest
import unittest
from unittest.mock import patch, Mock, call
from InquirerPy.base.control import Choice

mv = MenuView()
lv = LoginView()


def test_display_list(capsys, connection):
    ob_name = "employee"
    ob_list = connection.query(models.Employee).all()
    mv.show_list(ob_name, ob_list)

    assert "Liste des employees" in capsys.readouterr().out
    ob_name = "contract"
    ob_list = connection.query(models.Contract).all()
    mv.show_list(ob_name, ob_list)

    assert "Liste des contracts" in capsys.readouterr().out

    ob_name = "event"
    ob_list = connection.query(models.Event).all()
    mv.show_list(ob_name, ob_list)

    assert "Liste des events" in capsys.readouterr().out


def test_display_one_contract_event(capsys, connection, dummy_employee_commercial):
    customer = models.Client(
        name="customr1",
        email="customer1@example.com",
        telephone="1234567890",
        company_name="Company A",
        commercial_id=dummy_employee_commercial.id,
    )
    connection.add(customer)
    connection.commit()
    contract = models.Contract(
        client_id=customer.id,
        commercial_id=customer.commercial_id,
        total_amount=5000,
        due_amount=2000,
        status="signé",
    )
    connection.add(contract)
    connection.commit()
    event = models.Event(
        contract_id=contract.id,
        client_id=contract.client_id,
        start_date="01/02/2024",
        end_date="01/05/2024",
        support_id=None,
        location="Paris",
        total_attendees=20,
        notes="",
    )
    connection.add(event)
    connection.commit()
    mv.show_details("employee", dummy_employee_commercial)
    assert f"employee id :1" in capsys.readouterr().out

    mv.show_details("contract", contract)
    assert f"contract id :{contract.id}" in capsys.readouterr().out

    mv.show_details("event", event)
    assert f"event id :{event.id}" in capsys.readouterr().out


def test_login_display(monkeypatch):
    responses = iter(["gestion1@test.com", "Password12@"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(responses))
    assert lv.prompt_login_details() == ("gestion1@test.com", "Password12@")


@pytest.fixture
def mock_console(monkeypatch):
    mock_console = Mock()
    monkeypatch.setattr("epic_events.view.view.console", mock_console)
    return mock_console


def test_sucessful_logn(capsys):
    lv.successful_login()
    captured_stdout = capsys.readouterr().out
    assert "Vous êtes connectés" in captured_stdout


def test_read_condition(connection, monkeypatch):
    # breakpoint()
    employees = connection.query(models.Employee).all()
    choices = [
        Choice(value=employee.id, name=f"{employee.id} - {employee.name}")
        for employee in employees
    ]
    ob_name = "employee"
    monkeypatch.setattr("epic_events.data.dao.EmployeeDao.get_all", lambda _: employees)
    result = mv.read_condition(ob_name)
    # breakpoint()
    assert result == choices


def test_update_condition(connection, monkeypatch, dummy_employee_gestion):
    # breakpoint()
    employees = connection.query(models.Employee).all()
    choices = [
        Choice(value=employee.id, name=f"{employee.id} - {employee.name}")
        for employee in employees
    ]
    ob_name = "employee"
    monkeypatch.setattr("epic_events.data.dao.EmployeeDao.get_all", lambda _: employees)
    monkeypatch.setattr(
        "epic_events.data.dao.EmployeeDao.get_by_id",
        lambda self, employee_id: dummy_employee_gestion.id,
    )
    result = mv.update_condition(ob_name, dummy_employee_gestion.id)
    # breakpoint()
    assert result == choices


def test_prompt_for_ob_id(monkeypatch, dummy_employee_support):
    ob_name = "employee"
    action = "read"
    monkeypatch.setattr(
        "epic_events.view.view.inquirer.select.execute",
        lambda _: dummy_employee_support.id,
    )
    employee_id = dummy_employee_support.id
    result = mv.prompt_for_object_id(ob_name, action, employee_id)
    assert result == employee_id


def test_get_keys(monkeypatch, connection):
    ob_name = "employee"
    keys = models.Employee.__table__.columns.keys()
    result = mv.get_keys(ob_name)
    assert keys == result


def test_field_condition(monkeypatch, dummy_employee_gestion):
    key = "name"
    value = "gestion___1"
    monkeypatch.setattr(
        "epic_events.view.view.inquirer.text.execute",
        lambda prompt: "gestion___1",
    )
    breakpoint
    result = mv.field_conditions(key, dummy_employee_gestion.id)
    assert result == (key, value)


def test_datas_creation(monkeypatch, dummy_employee_gestion, capsys):
    ob_name = "employee"
    key = "name"
    value = "gestion___1"
    monkeypatch.setattr(
        "epic_events.view.view.MenuView.field_conditions",
        lambda self, k, employee_id: (key, value),
    )
    result = mv.propmt_for_data_creation(ob_name, dummy_employee_gestion.id)
    assert result == {key: value}


def test_check_date(monkeypatch):
    key = "start_date"
    format = "%d/%m/%Y"
    monkeypatch.setattr(
        "epic_events.view.view.inquirer.text.execute",
        lambda prompt: "02/02/2024",
    )
    breakpoint
    result = mv.check_date(key, format)

    assert "02/02/2024" == result


def test_confirmation_action(capsys):
    action = "create"
    ob_name = "employee"
    mv.action_confirmation(action, ob_name)
    captured_stdout = capsys.readouterr().out
    assert f"Nouveau employée a été crée." in captured_stdout


class TestViewWithInquirer(unittest.TestCase):
    @patch("epic_events.view.view.inquirer.select.execute")
    def test_main_menu(self, mocked_prompt):
        mocked_prompt.return_value = "employee"
        options = ["employee", "contract", "event", "client"]
        result = mv.main_menu(options)
        self.assertEqual(result, "employee")

    @patch("epic_events.view.view.inquirer.select.execute")
    def test_action_menu(self, mocked_prompt):
        ob_name = "employee"
        actions = [
            "read_all",
            "read_one",
            "create",
            "update",
            "delete",
            "read_no_support",
        ]
        mocked_prompt.return_value = "read_all"
        result = mv.actions_menu(ob_name, actions)

        self.assertEqual(result, "read_all")
