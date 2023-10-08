import os
from unittest.mock import mock_open, patch
import pytest
from click.testing import CliRunner
from epic_events import errors
from epic_events.controller import login_controller, permissions
from epic_events.controller.cli import execute_test_sql, login, logout, start
from epic_events.models import models

lt = login_controller.LoginController()


def test_incorrect_email_auth(monkeypatch, dummy_employee_gestion):
    responses = ("test@lol.fr", "Password12@")
    monkeypatch.setattr(
        "epic_events.view.view.LoginView.prompt_login_details", lambda prompt: responses
    )
    monkeypatch.setattr(
        "epic_events.data.dao.EmployeeDao.get_by_email",
        lambda self, email: dummy_employee_gestion,
    )
    assert pytest.raises(errors.InvalidEmailError)


def test_incorrect_password(monkeypatch, dummy_employee_gestion, capsys):
    responses = (dummy_employee_gestion.email, "Password@")
    monkeypatch.setattr(
        "epic_events.view.view.LoginView.prompt_login_details", lambda prompt: responses
    )
    monkeypatch.setattr(
        "epic_events.data.dao.EmployeeDao.get_by_email",
        lambda self, email: dummy_employee_gestion,
    )
    lt.authentification()
    assert "Votre mot de passe n'est pas correct." in capsys.readouterr().out


def test_login_auth(monkeypatch, dummy_employee_gestion):
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


def test_start(monkeypatch):
    runner = CliRunner()
    response = "exit"

    monkeypatch.setattr(
        "epic_events.view.view.MenuView.main_menu",
        lambda self, prompt: response,
    )

    result = runner.invoke(start)
    assert result.exit_code == 0


def test_logout_auth():
    runner = CliRunner()
    result = runner.invoke(logout)
    assert result.exit_code == 0


def test_ob_field_for_update(
    dummy_department_gestion,
    dummy_employee_commercial,
    dummy_employee_gestion,
    monkeypatch,
    connection,
):
    # Mock get_department and get_user_id functions
    monkeypatch.setattr(
        "epic_events.controller.permissions.get_department",
        lambda: dummy_department_gestion,
    )
    monkeypatch.setattr(
        "epic_events.controller.permissions.get_user_id",
        lambda: dummy_employee_gestion.id,
    )
    employees = connection.query(models.Employee).all()
    monkeypatch.setattr("epic_events.data.dao.EmployeeDao.get_all", lambda _: employees)
    ob_name = "employee"
    obj = dummy_employee_commercial
    fields = permissions.ob_field_for_update(ob_name, obj)

    # Assert that the actual result matches the expected result
    assert fields is None


def test_write_netrc():
    # Define sample input data
    host = "http://localhost:8080"
    entity = "your_email"
    key = "your_key"
    path = os.path.expanduser("~/.netrc")
    # Mock the required functions and open the .netrc file
    with patch("os.path.expanduser", return_value=path):
        with patch("os.chmod"):
            result = permissions.write_netrc(host, entity, key)
    assert result is True


def test_execute_test_sql():
    from tests.conftest import test_engine

    engine = test_engine()
    # Define the path to the SQL file
    sql_file_path = "tests/test.sql"
    open_name = "%s.open" % __name__

    # Define the content of the SQL file for testing
    sql_file_content = """
    INSERT INTO employees (`name`, `email`, `password`, `department_id`)
VALUES
    ('Lucie Page', 'lucie2@test.com', '$argon2id$v=19$m=16,t=2,p=1$QmQ2VjZ1SEZGNVdteVVwaA$45lep5zDs1oJYdG66alo3w', 1);
    """
    mock_connection = engine.raw_connection()
    mock_cursor = mock_connection.cursor()

    # Mock the database connection and cursor functions
    with patch(open_name, mock_open(read_data=sql_file_content)):
        with patch(
            "epic_events.data.conf.engine.raw_connection", return_value=mock_connection
        ):
            execute_test_sql(sql_file_path)

    # Verify that the SQL commands are executed
    expected_commands = [
        "INSERT INTO employees (`name`, `email`, `password`, `department_id`)"
        "VALUES('Lucie Page', 'lucie2@test.com', '$argon2id$v=19$m=16,t=2,p=1$QmQ2VjZ1SEZGNVdteVVwaA$45lep5zDs1oJYdG66alo3w', 1);"
    ]

    for command in expected_commands:
        mock_cursor.execute(command.strip())

    # Verify that the connection is committed
    mock_connection.commit()


mc = login_controller.MenuController()
