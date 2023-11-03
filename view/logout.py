import click

from view import cli
from controller.authentification import perform_logout


@cli.command
def logout():
    """
    Logout from the current session
    """
    if perform_logout() is True:
        click.echo("Logout successfull, goodbye !")

    else:
        click.echo("You are not logged in.")
