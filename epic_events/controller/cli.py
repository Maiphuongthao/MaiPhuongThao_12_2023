import click
from epic_events.controller.login_controller import LoginController, MenuController
from epic_events.controller.permissions import is_authenticated
from epic_events.data import conf


@click.group()
def cli():
    pass


@cli.command("login")
def login():
    login = LoginController()
    login.authentification()


@cli.command("start")
@is_authenticated
def start():
    menu = MenuController()
    menu.main_menu()


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
