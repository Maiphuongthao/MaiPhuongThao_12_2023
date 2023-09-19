import getpass
import click
from typing import Tuple
from rich.console import Console
from rich.table import Table
from epic_events.models import models
from InquirerPy import prompts, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator



ob_menu = {
    "employee": "employée",
    "client": "elient",
    "contract": "eontract",
    "event": "evènement",
}

actions = {
    "read": "consulter",
    "create": "créer",
    "update": "Modifier",
    "delete": "supprimer",
}


class LoginView:
    """
    Login functions gets username and password
    """

    def prompt_login_details(self) -> Tuple[str, str]:
        click.echo(
            "Saisissez votre email, votre mot de passe et tapez entrée, ou tapez sur ctrl+c pour sortir: "
        )
        email = getpass.getpass(prompt="Email:")
        password = getpass.getpass(prompt="Mot de passe:")
        return email, password

    def successful_login(self):
        click.echo("Vous êtes connectés.")


class MenuView:
    """Get main menu to chose which objet will be touch, once the action is chosen , the next menu will show with corresponding permissions list"""

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
            "read_one": f"Consulter d'un {ob_menu[ob_name]}",
            "create": f"Créer un {ob_menu[ob_name]}",
            "update": f"Modifier un {ob_menu[ob_name]}",
            "delete": f"Supprimer les {ob_menu[ob_name]}s",
            "read_no_support": f"Consulter les {ob_menu[ob_name]}s sans contact support",
            "read_no_signature": f"Consulter les {ob_menu[ob_name]}s non signés",
            "read_due_amount": f"Consulter les {ob_menu[ob_name]}s non soldés",
            "read_owned": f"Consulter les {ob_menu[ob_name]}s attribués",
        }
        choices = [action for action in actions if action is not None]
        menu = [
            Choice(action, name=f"{menu_text[action].capitalize()}s")
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

    def show_list(self, ob_name, ob_list):
       
        table = Table(title=f"Liste des {ob_name}s")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")
        if ob_name == "employee":
            table.add_column("Departement", style="green")
            for ob in ob_list:
                table.add_row(f"{ob.id}", ob.name, f"{ob.department['name']}")
            
        console = Console()
        console.print(table)





