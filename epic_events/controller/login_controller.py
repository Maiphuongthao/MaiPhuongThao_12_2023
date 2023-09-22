from epic_events.view import view
from epic_events.data.dao import EmployeeDao, EventDao, ContractDao, ClientDao

from epic_events.controller.permissions import (
    write_netrc,
    ob_for_main_menu,
    ob_for_actions_menu,
    get_user_id,
    ob_field_for_update,
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
event_dao = EventDao()
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
    def __init__(self):
        self.employee_id = get_user_id()

    @ob_for_main_menu
    def main_menu(self, objects: list = None):
        """
        First menu to select permission categorie
        """
        while True:
            choice = menu_view.main_menu(objects)
            if choice == "exit":
                exit()
            else:
                self.crud_menu(ob_name=choice)

    @ob_for_actions_menu
    def crud_menu(self, ob_name: str, actions: list = None):
        while True:
            choice = menu_view.actions_menu(ob_name, actions)
            if choice == "exit":
                break
            elif choice == "read_all":
                self.read_all(ob_name)
            elif choice == "read_one":
                ob = self.get_ob_by_id(ob_name, "read")
                self.read_one(ob_name, ob)
            elif choice == "create":
                self.create_one(ob_name)
            elif choice == "delete":
                self.delete(ob_name)
            elif choice == "update":
                obj = self.get_ob_by_id(ob_name, "update")
                self.update(ob_name, obj)

    def get_ob_by_id(self, ob_name, action):
        obj_id = menu_view.prompt_for_object_id(ob_name, action, self.employee_id)
        while True:
            if obj_id == "exit":
                break
            elif ob_name == "client":
                obj = client_dao.get_by_id(obj_id)
            elif ob_name == "contract":
                obj = contract_dao.get_by_id(obj_id)
            elif ob_name == "event":
                obj = event_dao.get_by_id(obj_id)
            elif ob_name == "employee":
                obj = employee_dao.get_by_id(obj_id)
            return obj

    def read_all(self, ob_name):
        obs_list = []
        if ob_name == "employee":
            obs_list = employee_dao.get_all()
        elif ob_name == "client":
            obs_list = client_dao.get_all()
        elif ob_name == "contract":
            obs_list = contract_dao.get_all()
        elif ob_name == "event":
            obs_list = event_dao.get_all()
        else:
            click.echo("Mauvaise choix, veuillez choisir une option correcte")
        menu_view.show_list(ob_name, obs_list)

    def read_one(self, ob_name, ob):
        menu_view.show_details(ob_name, ob)

    def create_one(self, ob_name):
        datas = menu_view.propmt_for_data_creation(ob_name, self.employee_id)
        if ob_name == "employee":
            p = PasswordHasher()
            datas["password"] = p.hash(datas["password"])
            employee_dao.add(datas)
        elif ob_name == "client":
            datas["commercial_id"] = self.employee_id
            client_dao.add(datas)
        elif ob_name == "contract":
            client = client_dao.get_by_id(datas["client_id"])
            datas["commercial_id"] = client.commercial_id
            contract_dao.add(datas)
        elif ob_name == "event":
            if datas["support_id"] == "":
                datas["support_id"] = None
            contract = contract_dao.get_by_id(datas["contract_id"])
            datas["client_id"] = contract.client_id
            event_dao.add(datas)
        else:
            click.echo("Mauvaise choix, veuillez choisir une option correcte")

        menu_view.action_confirmation(
            "create",
            ob_name,
        )

    def delete(self, ob_name):
        obj = self.get_ob_by_id(ob_name, "delete")
        self.read_one(ob_name, obj)
        if ob_name == "employee":
            employee_dao.delete(obj)
        else:
            click.echo("Pas de permission pour supprimé")
        menu_view.action_confirmation("delete", ob_name)

    def update(self, ob_name, obj):
        self.read_one(ob_name, obj)
        ob_fields = ob_field_for_update(ob_name, obj)
        field, value = self.get_field_value_from_prompt(obj, ob_fields)

        if ob_name == "employee":
            employee_dao.update(field, value, obj)
        if ob_name == "client": 
            client_dao.update(field, value, obj)
        if ob_name == "contract": 
            contract_dao.update(field, value, obj)
        if ob_name == "event": 
            event_dao.update(field, value, obj)
        
        menu_view.action_confirmation("update", ob_name)

