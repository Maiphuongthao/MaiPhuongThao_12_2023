from epic_events.models import models
from InquirerPy import prompts, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import getpass
import click
from typing import Tuple

class LoginView:
    """
    Login functions gets username and password 
    """
    def prompt_login_details(self) -> Tuple[str, str] :
        click.echo("Saisissez votre email, votre mot de passe et tapez entrée, ou tapez sur ctrl+c pour sortir: ") 
        email = getpass.getpass(prompt="Email:")
        password = getpass.getpass(prompt="Mot de passe:")
        return email, password
    
    def successful_login(self):
        click.echo("Vous êtes connectés.")
    

class MenuView:
    """Get main menu to chose which objet will be touch, once the action is chosen , the next menu will show with corresponding permissions list """
    
    def main_menu(self):
        menu = {
            "employees":"Employées",
            "clients":"Clients",
            "contracts":"Contracts",
            "events":"Evènements",
        }
        options=[]
        for op in menu:
            options.append(Choice(op, name=menu[op]))
        options.append(Separator())
        options.append(Choice(value=None, name="Exit"),)
        
        action = inquirer.select(message="Choisissez un menu:",
        choices=options,
        default="None",).execute()
        return action

    def menu_department_gestion(self):
        menu = {
            "create_employee":"Créer une employée",
            "update_employee":"Modifier une employée",
            "delete_employee":"Supprimer une employée",
            "create_contract":"Créer un contrat",
            "update_employee":"Modifier un contrat",
            "update_event":"Modififier un évènement",
            "create_employee":"Créer un employée",
        }
        pass

    def menu_department_commercial(self):
        pass

    def menu_department_support(self):
        pass