import click
from epic_events.controller.login_controller import LoginController

@click.group()
def cli():
    pass

@cli.command("login")
@click.option("--relogin", "-r", is_flag=True)
def login(relogin):
    login = LoginController()
    login.authentification(relogin)