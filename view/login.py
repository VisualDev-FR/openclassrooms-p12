import sys
from pwinput import pwinput
from authentification.login import perform_login
import click

from view import cli


@cli.command
@click.option("--email", help="Your authentification email", required=True)
def login(email):
    """
    Login with email and password.
    """
    password = pwinput("password : ")

    logged_in_employee = perform_login(email, password)

    if not logged_in_employee:
        click.echo("Invalid credentials")
        return

    click.echo(f"Welcome {logged_in_employee.full_name} !")
