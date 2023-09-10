from epic_events.models import models
from InquirerPy import prompts, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import getpass

class LoginView:
    """
    Login functions gets username and password 
    """
    def login_get_username_and_password(self):
        print("\n\n\n")
        print("------------------------------------------------".center(20))
        print("------------------------------------------------".center(20))
        print("--------------------Epic Events-----------------".center(20))
        print("------------------------------------------------".center(20))
        print("------------------------------------------------".center(20))
        print("\n\n\n")

        print("Saisissez votre email, votre mot de passe et tapez entrée, ou tapez sur ctrl+c pour sortir: ") 
        email = getpass.getpass(prompt="Email:")
        password = getpass.getpass(prompt="Mot de passe:")
        return email, password
    

class MenuView:

    def main_menu(self):
        pass

    def menu_department_gestion(self):
        pass

    def menu_department_commercial(self):
        pass

    def menu_department_support(self):
        pass