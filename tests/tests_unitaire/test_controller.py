from click.testing import CliRunner
from epic_events.controller.cli import login, logout, start
import pytest
from epic_events import errors


# def test_cli_running_login(monkeypatch, dummy_employee_gestion, connection):
#     runner = CliRunner()
#     responses = iter([dummy_employee_gestion.email, "Password12@"])
#     monkeypatch.setattr('getpass.getpass', lambda prompt: next(responses))
#     assert login() == (dummy_employee_gestion.email, dummy_employee_gestion.password)


def test_incorrect_email_auth(monkeypatch, dummy_employee_gestion, connection):
    runner = CliRunner()
    responses = ("test@lol.fr", "Password12@")
    monkeypatch.setattr(
        "epic_events.view.view.LoginView.prompt_login_details", lambda prompt: responses
    )
    monkeypatch.setattr(
        "epic_events.data.dao.EmployeeDao.get_by_email",
        lambda self, email: dummy_employee_gestion,
    )

    result = runner.invoke(login)
    assert result.exit_code == 0
    assert pytest.raises(errors.InvalidEmailError)
    

def test_login_auth(monkeypatch, dummy_employee_gestion, connection):
    runner = CliRunner()
    responses = (dummy_employee_gestion.email, "Password12@")
    monkeypatch.setattr(
        "epic_events.view.view.LoginView.prompt_login_details", lambda prompt: responses
    )
    monkeypatch.setattr(
        "epic_events.data.dao.EmployeeDao.get_by_email",
        lambda self, email: dummy_employee_gestion,
    )

    result = runner.invoke(login)
    assert result.exit_code == 0
    assert "Vous êtes connectés." in result.output.strip()

def test_start(monkeypatch, connection):
    runner = CliRunner()
    response = "exit"

    monkeypatch.setattr(
        "epic_events.view.view.MenuView.main_menu",
        lambda self,prompt: response,
    )
    # monkeypatch.setattr(
        # "epic_events.controller.login_controller.MenuController.crud_menu",
        # lambda self, ob_name: setattr(self, )
    # )
    result = runner.invoke(start)
    assert result.exit_code == 0

def test_logout_auth():
    runner = CliRunner()
    result = runner.invoke(logout)
    assert result.exit_code == 0




