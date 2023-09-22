import getpass
import click
from datetime import datetime
from typing import Tuple
from rich.console import Console
from rich.table import Table
from rich.text import Text
from epic_events.data.dao import (
    DepartmentDao,
    ClientDao,
    ContractDao,
    EmployeeDao,
    EventDao,
)
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import PasswordValidator, EmptyInputValidator, NumberValidator


ob_menu = {
    "employee": "employée",
    "client": "client",
    "contract": "contract",
    "event": "evènement",
}

actions = {
    "read": "consulter",
    "create": "créer",
    "update": "Modifier",
    "delete": "supprimer",
}

attributes = {
    "name": "Nom et prénom",
    "email": "Email",
    "password": "Mot de passe",
    "department_id": "Departement",
    "telephone": "Numéros de téléphone",
    "company_name": "Nom de l'entreprise",
    "client_id": "Id de client",
    "total_amount": "Montant total",
    "due_amount": "Montant restant",
    "status": "Statut du contrat - signé/ en attend",
    "contract_id": "S du contrat",
    "start_date": "Date de début (DD/MM/YYYY)",
    "end_date": "Date de fin (DD/MM/YYYY)",
    "support_id": "Id du support",
    "location": "Location",
    "total_attendees": "Nombre de participant",
    "notes": "Notes",
}

depart_dao = DepartmentDao()
client_dao = ClientDao()
contract_dao = ContractDao()
event_dao = EventDao()
employee_dao = EmployeeDao()
console = Console()


class LoginView:
    """
    Login functions gets username and password
    """

    def prompt_login_details(self) -> Tuple[str, str]:
        text = Text("Entrez votre email et votre mot de passe ou ctrl+c pour sortir")
        text.stylize("bold magenta")
        console.print(text)
        email = getpass.getpass(prompt="Email:")
        password = getpass.getpass(prompt="Mot de passe:")
        return email, password

    def successful_login(self):
        text = Text("Vous êtes connectés.")
        text.stylize("bole green")
        console.print(text)


class MenuView:
    """Get main menu to chose which objet will be touch
    once the action is chosen
    the next menu will show with corresponding permissions list"""

    def __init__(self):
        self.employee_view = EmployeeView()
        self.client_view = ClientView()
        self.contract_view = ContractView()
        self.event_view = EventView()

    def main_menu(self, objects):
        options = [obj for obj in objects if obj is not None]

        menu = [Choice(obj, name=f"{ob_menu[obj].capitalize()}s") for obj in options]
        menu.append(Separator())
        menu.append(
            Choice(value="exit", name="Quitter"),
        )

        action = inquirer.select(
            message="Choisissez un menu:",
            choices=menu,
            default="None",
        ).execute()
        return action

    def actions_menu(self, ob_name, actions):
        menu_text = {
            "read_all": f"Consulter les {ob_menu[ob_name]}s",
            "read_one": f"Consulter un {ob_menu[ob_name]}",
            "create": f"Créer un {ob_menu[ob_name]}",
            "update": f"Modifier un {ob_menu[ob_name]}",
            "delete": f"Supprimer un {ob_menu[ob_name]}",
            "read_no_support": f"Consulter les {ob_menu[ob_name]}s sans contact support",
            "read_no_signature": f"Consulter les {ob_menu[ob_name]}s non signés",
            "read_due_amount": f"Consulter les {ob_menu[ob_name]}s non soldés",
            "read_owned": f"Consulter les {ob_menu[ob_name]}s attribués",
        }
        choices = [action for action in actions if action is not None]
        menu = [
            Choice(action, name=f"{menu_text[action].capitalize()}")
            for action in choices
        ]
        menu.append(Separator())
        menu.append(
            Choice(value="exit", name="Retourner"),
        )
        action = inquirer.select(
            message="Choisissez un menu:",
            choices=menu,
            default="None",
        ).execute()
        return action

    def read_condition(self, ob_name):
        if ob_name == "employee":
            choices = [
                Choice(value=employee.id, name=f"{employee.id} - {employee.name}")
                for employee in employee_dao.get_all()
            ]
        elif ob_name == "client":
            choices = [
                Choice(value=client.id, name=f"{client.id} - {client.name}")
                for client in client_dao.get_all()
            ]
        elif ob_name == "contract":
            choices = [
                Choice(
                    value=contract.id,
                    name=f"{contract.id} - client_id : {contract.client_id} - total_amount: {contract.total_amount}",
                )
                for contract in contract_dao.get_all()
            ]
        elif ob_name == "event":
            choices = [
                Choice(
                    value=event.id,
                    name=f"{event.id} - client_id: {event.client_id} - start_date: {event.start_date} - {event.location}",
                )
                for event in event_dao.get_all()
            ]
        return choices

    def update_condition(self, ob_name, employee_id):
        employee = employee_dao.get_by_id(employee_id)
        # breakpoint()
        if ob_name == "employee":
            choices = [
                Choice(value=employee.id, name=f"{employee.id} - {employee.name}")
                for employee in employee_dao.get_all()
            ]
        elif ob_name == "client":
            choices = [
                Choice(value=client.id, name=f"{client.id} - {client.name}")
                for client in client_dao.get_by_commercial_id(employee_id)
            ]
        elif ob_name == "contract":
            if employee.department.name == "Gestion":
                choices = [
                    Choice(
                        value=contract.id,
                        name=f"{contract.id} - client_id : {contract.client_id} - total_amount: {contract.total_amount}",
                    )
                    for contract in contract_dao.get_unsigned_contracts()
                ]
            elif employee.department.name == "Commercial":
                choices = [
                    Choice(
                        value=contract.id,
                        name=f"{contract.id} - client_id : {contract.client_id} - total_amount: {contract.total_amount}",
                    )
                    for contract in contract_dao.get_by_commercial_id(employee_id)
                ]
        elif ob_name == "event":
            if employee.department.name == "Gestion":
                choices = [
                    Choice(
                        value=event.id,
                        name=f"{event.id} - client_id: {event.client_id} - start_date: {event.start_date} - {event.location}",
                    )
                    for event in event_dao.get_no_support()
                ]
            elif employee.department.name == "Support":
                choices = [
                    Choice(
                        value=event.id,
                        name=f"{event.id} - client_id: {event.client_id} - start_date: {event.start_date} - {event.location}",
                    )
                    for event in event_dao.get_by_support_id(employee_id)
                ]

        return choices

    def prompt_for_object_id(self, ob_name, action, employee_id):
        """
        Ask to chose an id for action corresponding
        """

        if action in ["read", "read_all"]:
            choices = self.read_condition(ob_name)
        elif action == "update":
            # breakpoint()
            choices = self.update_condition(ob_name, employee_id)
        elif action == "delete":
            if ob_name == "employee":
                choices = [
                    Choice(value=employee.id, name=f"{employee.id} - {employee.name}")
                    for employee in employee_dao.get_all()
                ]
            else:
                click.echo("Pas de permission")

        elif action == "read_no_support":
            if ob_name == "employee":
                choices = [
                    Choice(
                        value=event.id,
                        name=f"{event.id} - client_id: {event.client_id} - start_date: {event.start_date} - {event.location}",
                    )
                    for event in event_dao.get_no_support()
                ]
            else:
                click.echo("Pas de permission")

        elif action == "read_no_signature":
            if ob_name == "commercial":
                choices = [
                    Choice(
                        value=contract.id,
                        name=f"{contract.id} - client_id : {contract.client_id} - total_amount: {contract.total_amount}",
                    )
                    for contract in contract_dao.get_unsigned_contracts()
                ]
            else:
                click.echo("Pas de permission")

        elif action == "read_due_amount":
            if ob_name == "Commercial":
                choices = [
                    Choice(
                        value=contract.id,
                        name=f"{contract.id} - client_id : {contract.client_id} - total_amount: {contract.total_amount}",
                    )
                    for contract in contract_dao.get_due_amount_higher_than_zero()
                ]
            else:
                click.echo("Pas de permission")
        else:
            click.echo("Pas de bon option")

        choices.append(Separator())
        choices.append(
            Choice(value="exit", name="Retourner"),
        )

        obj_id = inquirer.select(
            message=f"Choisir id du {ob_menu[ob_name]} à {actions[action]}:",
            choices=choices,
            default=None,
        ).execute()
        # breakpoint()
        return obj_id

    def show_list(self, ob_name, ob_list):
        # show table of list corresponding
        table = Table(title=f"Liste des {ob_name}s")
        if ob_name == "employee":
            table = self.employee_view.table_employee(table)
            for ob in ob_list:
                self.employee_view.table_row(table, ob)
        if ob_name == "client":
            table = self.client_view.table_client(table)
            for ob in ob_list:
                self.client_view.table_row(table, ob)
        if ob_name == "contract":
            table = self.contract_view.table_contract(table)
            for ob in ob_list:
                self.contract_view.table_row(table, ob)
        if ob_name == "event":
            table = self.event_view.table_event(table)
            for ob in ob_list:
                self.event_view.table_row(table, ob)

        console.print(table)

    def show_details(self, ob_name, ob):
        # show table of id corresponding
        table = Table(title=f"{ob_name} id :{ob.id}")
        if ob_name == "employee":
            table = self.employee_view.table_employee(table)
            self.employee_view.table_row(table, ob)

        if ob_name == "client":
            table = self.client_view.table_client(table)
            self.client_view.table_row(table, ob)

        if ob_name == "contract":
            table = self.contract_view.table_contract(table)
            self.contract_view.table_row(table, ob)

        if ob_name == "event":
            table = self.event_view.table_event(table)
            self.event_view.table_row(table, ob)

        console.print(table)

    def get_keys(self, ob_name):
        keys = []
        if ob_name == "employee":
            keys = employee_dao.get_columns_key()
        elif ob_name == "client":
            keys = client_dao.get_columns_key()
        elif ob_name == "event":
            keys = event_dao.get_columns_key()
            keys.remove("client_id")
        elif ob_name == "contract":
            keys = contract_dao.get_columns_key()
        return keys

    def field_conditions(self, key, employee_id):
        if key == "password":
            value = self.employee_view.prompt_password(key)
        elif key in ["total_amount", "due_amount"]:
            value = self.contract_view.prompt_prices(key)
        elif key == "total_attendees":
            value = self.event_view.prompt_attendees(key)
        elif key == "client_id":
            value = self.contract_view.prompt_client(key)

        elif key == "contract_id":
            value = self.event_view.prompt_contract_id(key, employee_id)
        elif key == "status":
            value = self.contract_view.prompt_status(key)
        elif key == "department_id":
            value = self.employee_view.prompt_department(key)
        elif key in ["notes", "support_id"]:
            value = inquirer.text(message=f"{attributes[key]}:").execute()
        elif key in ["start_date", "end_date"]:
            # datas[key] = self.date_inquirer(key)
            format = "%d/%m/%Y"
            value = self.check_date(key, format)
        else:
            value = inquirer.text(
                message=f"{attributes[key]}:",
                validate=EmptyInputValidator("Le champ ne peut pas être vide"),
            ).execute()
        return key, value

    def propmt_for_data_creation(self, ob_name, employee_id):
        text = Text(f"Entrez les données du {ob_menu[ob_name]}:")
        text.stylize("magenta")
        console.print(text)
        datas = {}
        keys = self.get_keys(ob_name)

        for key in keys:
            if key in attributes:
                key, datas[key] = self.field_conditions(key, employee_id)
        return datas

    def prompt_for_update(self, ob, fields, employee_id):
        fields = fields if fields else [field for field in ob.__dict__.keys()]
        choices = [
            Choice(field, name=f"{field}: {value}")
            for field, value in ob.__dict__.items()
            if (field in attributes)
        ]
        choices.append(Separator())
        choices.append(
            Choice(value="exit", name="Retourner"),
        )

        modify_field = inquirer.select(
            message="Veuillez selectionner le champs à modifier:",
            choices=choices,
            default=None,
        ).execute()
        modify_field, new_value = self.field_conditions(modify_field, employee_id)
        return modify_field, new_value

    def check_date(self, key, format):
        while True:
            res = inquirer.text(
                message=f"{attributes[key]}:",
                validate=EmptyInputValidator(
                    "Veuillez mettre une date correspond au format:" "jour/mois/année"
                ),
            ).execute()
            try:
                datetime.strptime(res, format)
                break
            except ValueError:
                print("Veuillez renoter la date avec le bon format DD/MM/YYYY")
        return res

    def action_confirmation(self, action, ob_name):
        if action == "create":
            text = Text(f"Nouveau {ob_menu[ob_name]} a été crée:")
        if action == "update":
            text = Text(f"Le {ob_menu[ob_name]} a été modifié:")
        if action == "delete":
            text = Text(f"Le {ob_menu[ob_name]} a été supprimé")

        text.stylize("green")
        console.print(text)


class EmployeeView:
    def table_employee(self, table):
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Departement", style="green")
        return table

    def table_row(self, table, ob):
        return table.add_row(f"{ob.id}", ob.name, ob.email, f"{ob.department.name}")

    def prompt_password(self, key):
        return inquirer.secret(
            message=f"Entrez nouvelle {key}:",
            validate=PasswordValidator(
                length=8,
                cap=True,
                special=True,
                number=True,
                message="Password doit contient:"
                "8 caractéres"
                "une majuscule"
                "un caractère special"
                "un chiffre",
            ),
        ).execute()

    def prompt_department(self, key):
        return inquirer.select(
            message=f"Sélectionner un {key}:",
            choices=[
                Choice(value=1, name="Gestion"),
                Choice(value=2, name="Commercial"),
                Choice(value=3, name="Support"),
            ],
            default=None,
        ).execute()


class ClientView:
    def table_client(self, table):
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta", no_wrap=True)
        table.add_column("Email", style="green", no_wrap=True)
        table.add_column("Téléphone", style="green")
        table.add_column("Nom de l'entreprise", style="green")
        table.add_column("Contact commercial", style="green")
        table.add_column("Date de création", style="magenta")
        return table

    def table_row(self, table, ob):
        return table.add_row(
            f"{ob.id}",
            ob.name,
            ob.email,
            ob.telephone,
            ob.company_name,
            f"{ob.commercial.name}",
            f"{ob.created_date}",
        )


class ContractView:
    def table_contract(self, table):
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Client", style="magenta", no_wrap=True)
        table.add_column("Contact Commercial", style="green")
        table.add_column("Montant total", style="green")
        table.add_column("Montant restant", style="yellow")
        table.add_column("Date de création", style="yellow")
        table.add_column("Statut", style="red")
        return table

    def table_row(self, table, ob):
        return table.add_row(
            f"{ob.id}",
            f"{ob.client.name}",
            f"{ob.commercial.name}",
            f"{ob.total_amount}",
            f"{ob.due_amount}",
            f"{ob.created_date}",
            ob.status,
        )

    def prompt_prices(self, key):
        return inquirer.number(
            message=f"New {key}:",
            float_allowed=True,
            validate=EmptyInputValidator(
                "Chiffre décimaux obligatoire" "séparés par un point. exp: 1.00"
            ),
        ).execute()

    def prompt_client(self, key):
        return inquirer.select(
            message=f"Sélectionner un {key}:",
            choices=[
                Choice(value=client.id, name=f"{client.id} - {client.name}")
                for client in client_dao.get_all()
            ],
            default=None,
        ).execute()

    def prompt_status(self, key):
        return inquirer.select(
            message=f"Sélectionner un {key}:",
            choices=[
                Choice(value="signé", name="Signé"),
                Choice(value="en attend", name="En attend"),
                Choice(value="soldé", name="Tout payé"),
                Choice(value="pas soldé", name="Pas encore tout payé"),
            ],
            default=None,
        ).execute()


class EventView:
    def table_event(self, table):
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Contract ID", style="magenta", no_wrap=True)
        table.add_column("Client", style="green")
        table.add_column("Contact de client", style="green")
        table.add_column("Location", style="green")
        table.add_column("Nombre de participants", style="green")
        table.add_column("Date de début", style="yellow")
        table.add_column("Date de fin", style="yellow")
        table.add_column("Notes", style="white")
        return table

    def table_row(self, table, ob):
        return table.add_row(
            f"{ob.id}",
            f"{ob.contract_id}",
            f"{ob.client.name}",
            f"{ob.client.email}, {ob.client.telephone}",
            f"{ob.location}",
            f"{ob.total_attendees}",
            f"{ob.start_date}",
            f"{ob.end_date}",
            ob.notes,
        )

    def prompt_attendees(self, key):
        return inquirer.number(
            message=f"Entrez nouvelle {key}:",
            min_allowed=2,
            validate=EmptyInputValidator("Le champs ne peut pas être vide."),
        ).execute()

    def prompt_contract_id(self, key, employee_id):
        return inquirer.select(
            message=f"Sélectionner un {key}:",
            choices=[
                Choice(
                    value=contract.id,
                    name=f"{contract.id} - {contract.total_amount} - {contract.status}",
                )
                for contract in contract_dao.get_signed_contract(employee_id)
            ],
            default=None,
        ).execute()
