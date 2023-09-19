from epic_events.view import view
from epic_events.data.dao import EmployeeDao, EventDao, ContractDao, ClientDao
from epic_events.controller.permissions import (
    write_netrc,
    ob_for_main_menu,
    ob_for_actions_menu,
)
from argon2 import PasswordHasher, exceptions
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timezone, timedelta
import jwt
import click

import os
from dotenv import load_dotenv

load_dotenv()

netrc_host = os.getenv("HOST")
login_view = view.LoginView()
menu_view = view.MenuView()
employee_dao = EmployeeDao()
client_dao = ClientDao()
event_dao = ClientDao()
contract_dao = ContractDao()

class LoginController:
    def __init__(self):
        self.menu_controller = MenuController()

    def authentification(self):
        """
        verify email and password then create a token with RS256 - asymmetric algorithm
        """
        (email, password) = login_view.prompt_login_details()
        try:
            employee = employee_dao.get_by_email(email)
        except IndexError:
            print("\nVotre addresse email n'est pas correct.")
            exit()
        try:
            h = PasswordHasher()
            # breakpoint()
            h.verify(employee.password, password)
            private_key = os.getenv("PRIVATE_KEY")
            serialize_key = serialization.load_pem_private_key(
                private_key.encode(), password=None
            )

            payload = {
                "email": email,
                "departement_id": employee.department_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24),
            }
            token = jwt.encode(payload=payload, key=serialize_key, algorithm="RS256")
            # breakpoint()
            write_netrc(netrc_host, email, token)
            login_view.successful_login()
        except exceptions.VerifyMismatchError:
            print("Votre mot de passe n'est pas correct.")


class MenuController:
    def __init__(self) -> None:
        pass

    @ob_for_main_menu
    def main_menu(self, objects:list = None):
        """
        First menu to select permission categorie
        """
        while True:
            choice = menu_view.main_menu(objects)
            if choice == "exit":
                exit()
            else:
                self.crud_menu(ob_name = choice)
                

    @ob_for_actions_menu
    def crud_menu(self, ob_name: str, actions: list = None):
       
        while True:
            choice = menu_view.actions_menu(ob_name, actions)
            if choice == "exit":
                break
            elif choice == "read_all":
                self.read_all(ob_name)
                

    def read_all(self, ob_name):
        obs_list = []
        if ob_name == "employee":
            obs_list = employee_dao.get_all()
        elif ob_name == "client":
            obs_list = client_dao.get_all()
        elif ob_name == "event":
            obs_list = event_dao.get_all()
        elif ob_name == "contract":
            obs_list = contract_dao.get_all()
        menu_view.show_list(ob_name, obs_list)
