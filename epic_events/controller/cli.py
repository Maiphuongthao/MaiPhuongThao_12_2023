import click
from epic_events.controller.login_controller import LoginController, MenuController
from epic_events.controller.permissions import is_authenticated
from epic_events.data import conf


@click.group()
def cli():
    pass


# commande to activate login authentification
@cli.command("login")
def login():
    login = LoginController()
    login.authentification()


# commande to start manu
@cli.command("start")
@is_authenticated
def start():
    menu = MenuController()
    menu.main_menu()


# commande to logout with delete none to netrc file
@cli.command("logout")
@is_authenticated
def logout():
    menu = MenuController()
    menu.logout()


# ad 1st info to database to test
def execute_test_sql(file):
    f = open(file, "r")
    sql_file = f.read()
    f.close()

    connection = conf.engine.raw_connection()
    cursor = connection.cursor()
    commands = sql_file.split(";")
    for command in commands:
        try:
            if command.strip() != "":
                cursor.execute(command)
        except IOError as msg:
            print(f"Command skipped: {msg}")

    connection.commit()
