from epic_events.view import view
from epic_events.data.dao import EmployeeDao, EventDao, ContractDao, ClientDao
from epic_events.data.conf import key
from epic_events import errors

from epic_events.controller.permissions import (
    write_netrc,
    ob_for_main_menu,
    ob_for_actions_menu,
    ob_field_for_update,
    get_user_id,
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


class LoginController:
    def __init__(self):
        self.menu_controller = MenuController()
        self.login_view = view.LoginView()
        self.employee_dao = EmployeeDao()

    def authentification(self):
        """
        verify email and password then create a token with RS256
        - asymmetric algorithm
        """
        (email, password) = self.login_view.prompt_login_details()
        try:
            employee = self.employee_dao.get_by_email(email)
            try:
                h = PasswordHasher()
                h.verify(employee.password, password)
                serialize_key = serialization.load_ssh_private_key(
                    key.encode(), password=None
                )

                payload = {
                    "email": email,
                    "departement_id": employee.department_id,
                    "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24),
                }
                token = jwt.encode(
                    payload=payload, key=serialize_key, algorithm="RS256"
                )
                write_netrc(netrc_host, email, token)
                self.login_view.successful_login()
            except exceptions.VerifyMismatchError:
                print("Votre mot de passe n'est pas correct.")
        except errors.InvalidEmailError:
            print("\nVotre addresse email n'est pas correct.")
            exit()


class MenuController:
    def __init__(self):
        self.menu_view = view.MenuView()
        self.employee_dao = EmployeeDao()
        self.client_dao = ClientDao()
        self.event_dao = EventDao()
        self.contract_dao = ContractDao()

    @ob_for_main_menu
    def main_menu(self, objects: list = None):
        """
        First menu to select permission categorie
        """
        while True:
            choice = self.menu_view.main_menu(objects)
            if choice == "exit":
                exit()
            else:
                self.crud_menu(ob_name=choice)

    def logout(self):
        write_netrc(netrc_host, "None", "None")
        print("Vous êtes déconnecté")

    def crud_menu(self, ob_name: str):
        actions = ob_for_actions_menu(ob_name)
        while True:
            choice = self.menu_view.actions_menu(ob_name, actions)
            if choice == "exit":
                break
            elif choice == "read_all":
                self.read_all(ob_name)
            elif choice == "read_one":
                ob = self.get_ob_by_id(ob_name, "read")
                if ob:
                    self.read_one(ob_name, ob)
                else:
                    self.crud_menu(ob_name)
            elif choice == "create":
                self.create_one(ob_name)
            elif choice == "delete":
                self.delete(ob_name)
            elif choice == "update":
                obj = self.get_ob_by_id(ob_name, "update")
                if obj:
                    self.update(ob_name, obj)
                else:
                    self.crud_menu(ob_name)
            elif choice == "read_no_support":
                self.read_no_support(ob_name)
            elif choice == "read_no_signature":
                self.read_no_signature(ob_name)
            elif choice == "read_due_amount":
                self.read_due_amount(ob_name)
            elif choice == "read_owned":
                self.read_owned(ob_name)
            else:
                click.echo("Not allowed.")

    def get_ob_by_id(self, ob_name, action):
        employee_id = get_user_id()
        obj_id = self.menu_view.prompt_for_object_id(ob_name, action, employee_id)
        while True:
            if obj_id == "exit":
                break
            elif ob_name == "client":
                obj = self.client_dao.get_by_id(obj_id)
            elif ob_name == "contract":
                obj = self.contract_dao.get_by_id(obj_id)
            elif ob_name == "event":
                obj = self.event_dao.get_by_id(obj_id)
            elif ob_name == "employee":
                obj = self.employee_dao.get_by_id(obj_id)
            return obj

    def read_all(self, ob_name):
        obs_list = []
        if ob_name == "employee":
            obs_list = self.employee_dao.get_all()
        elif ob_name == "client":
            obs_list = self.client_dao.get_all()
        elif ob_name == "contract":
            obs_list = self.contract_dao.get_all()
        elif ob_name == "event":
            obs_list = self.event_dao.get_all()
        else:
            click.echo("Mauvais choix, veuillez choisir une option correcte")
        self.menu_view.show_list(ob_name, obs_list)

    def read_one(self, ob_name, ob):
        self.menu_view.show_details(ob_name, ob)

    def create_one(self, ob_name):
        employee_id = get_user_id()
        datas = self.menu_view.propmt_for_data_creation(ob_name, employee_id)
        if ob_name == "employee":
            p = PasswordHasher()
            datas["password"] = p.hash(datas["password"])
            self.employee_dao.add(datas)
        elif ob_name == "client":
            datas["commercial_id"] = employee_id
            self.client_dao.add(datas)
        elif ob_name == "contract":
            client = self.client_dao.get_by_id(datas["client_id"])
            datas["commercial_id"] = client.commercial_id
            self.contract_dao.add(datas)
        elif ob_name == "event":
            if datas["support_id"] == "":
                datas["support_id"] = None
            contract = self.contract_dao.get_by_id(datas["contract_id"])
            datas["client_id"] = contract.client_id
            self.event_dao.add(datas)
        else:
            click.echo("Mauvaise choix, veuillez choisir une option correcte")

        self.menu_view.action_confirmation(
            "create",
            ob_name,
        )

    def delete(self, ob_name):
        obj = self.get_ob_by_id(ob_name, "delete")
        self.read_one(ob_name, obj)
        if ob_name == "employee":
            self.employee_dao.delete(obj)
        else:
            click.echo("Pas de permission pour supprimé")
        self.menu_view.action_confirmation("delete", ob_name)

    def update(self, ob_name, obj):
        employee_id = get_user_id()
        self.read_one(ob_name, obj)
        ob_fields = ob_field_for_update(ob_name, obj)
        field, value = self.menu_view.prompt_for_update(obj, ob_fields, employee_id)
        while True:
            if "exit" in [field, value]:
                break
            else:
                self.update_action(ob_name, obj, field, value)
                break

    def update_action(self, ob_name, obj, field, value):
        if ob_name == "employee":
            self.employee_dao.update(field, value, obj)
        if ob_name == "client":
            self.client_dao.update(field, value, obj)
        if ob_name == "contract":
            self.contract_dao.update(field, value, obj)
        if ob_name == "event":
            self.event_dao.update(field, value, obj)
        self.menu_view.action_confirmation("update", ob_name)

    def read_no_support(self, ob_name):
        events = self.event_dao.get_no_support()
        self.menu_view.show_list(ob_name, events)

    def read_no_signature(self, ob_name):
        contracts = self.contract_dao.get_unsigned_contracts()
        self.menu_view.show_list(ob_name, contracts)

    def read_due_amount(self, ob_name):
        contracts = self.contract_dao.get_due_amount_higher_than_zero()
        self.menu_view.show_list(ob_name, contracts)

    def read_owned(self, ob_name):
        employee_id = get_user_id()
        if ob_name == "contracts":
            ob_list = self.contract_dao.get_by_commercial_id(employee_id)
        elif ob_name == "event":
            ob_list = self.event_dao.get_by_support_id(employee_id)
        elif ob_name == "clent":
            ob_list = self.client_dao.get_by_commercial_id(employee_id)
        self.menu_view.show_list(ob_name, ob_list)
