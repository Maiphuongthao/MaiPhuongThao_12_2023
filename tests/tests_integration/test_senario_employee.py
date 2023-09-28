from click.testing import CliRunner
from epic_events.controller.cli import login, logout, start
from epic_events.controller.login_controller import MenuController
import pytest
from epic_events import errors


class TestIntergation:
    def test_employee_read_create_senario(
        self, monkeypatch, dummy_employee_gestion, connection
    ):
        """
        Create senario login/start/logout with clie and create, 
        update and delete an employee
        """
        runner = CliRunner()
        mc = MenuController()

        responses = ("test@lol.fr", "Password12@")

        monkeypatch.setattr(
            "epic_events.view.view.LoginView.prompt_login_details",
            lambda prompt: responses,
        )
        monkeypatch.setattr(
            "epic_events.data.dao.EmployeeDao.get_by_email",
            lambda self, email: dummy_employee_gestion,
        )
        result = runner.invoke(login)
        assert result.exit_code == 0
        assert pytest.raises(errors.InvalidEmailError)

        monkeypatch.setattr(
            "epic_events.view.view.LoginView.prompt_login_details",
            lambda prompt: responses,
        )
        monkeypatch.setattr(
            "epic_events.data.dao.EmployeeDao.get_by_email",
            lambda self, email: dummy_employee_gestion,
        )

        responses = (dummy_employee_gestion.email, "Password12@")
        result = runner.invoke(login)

        assert result.exit_code == 0
        assert "Vous êtes connectés." in result.output.strip()

        response = "employee"
        actions = [
            "read_all",
            "read_one",
            "create",
            "update",
            "delete",
            "read_no_support",
        ]

        monkeypatch.setattr(
            "epic_events.view.view.MenuView.main_menu",
            lambda self, prompt: response,
        )
        monkeypatch.setattr(
            "epic_events.controller.login_controller.ob_for_actions_menu",
            lambda prompt: actions,
        )
        # read
        monkeypatch.setattr(
            "epic_events.view.view.MenuView.actions_menu",
            lambda self, ob_name, prompt: "read_all",
        )

        # create
        monkeypatch.setattr(
            "epic_events.view.view.MenuView.actions_menu",
            lambda self, ob_name, prompt: "create",
        )

        datas = {
            "name": "gestion2",
            "email": "gestion2@test.com",
            "password": "Pasword12@",
            "department_id": 2,
        }
        monkeypatch.setattr(
            "epic_events.view.view.MenuView.propmt_for_data_creation",
            lambda ob_name, employee_id: datas,
        )
        monkeypatch.setattr(
            "epic_events.controller.login_controller.get_user_id",
            lambda : dummy_employee_gestion.id,
        )
        monkeypatch.setattr(
            "epic_events.data.dao.session.add",
            lambda datas: connection,
        )
        
        # exit
                
        monkeypatch.setattr(
            "epic_events.view.view.MenuView.actions_menu",
            lambda self, ob_name, prompt: "exit",
        )
        monkeypatch.setattr(
            "epic_events.view.view.MenuView.main_menu",
            lambda self,prompt: "exit",
        )

        result = runner.invoke(start)
        assert result.exit_code == 0

        
        result = runner.invoke(logout)
        assert result.exit_code == 0
        
