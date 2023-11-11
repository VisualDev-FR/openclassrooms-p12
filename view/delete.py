import click
from sqlalchemy.exc import IntegrityError

from view import cli
from view.read import generic_read
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event
from controller.cascade import CascadeDetails
from controller.database import create_session
from controller.managers import (
    Manager,
    EmployeeManager,
    ClientsManager,
    ContractsManager,
    EventsManager,
)


@cli.group()
def delete():
    """
    Delete an existing entry.
    """
    pass


def generic_delete(manager: Manager, model: type, query: str):
    """
    Generic view to retreive datas and display them in a tabulated view.

    Args:
    * ``manager``: the manager of the accessed datas
    * ``model``: the model of the accessed datas
    * ``query``: a string containing a query to apply on the given manager
    """
    try:
        full_query = f"{model.__name__}.{query}"
        parsed_query = eval(full_query)

    except (NameError, AttributeError, SyntaxError):
        click.echo(f"query error: {full_query}")
        return

    deleted_objects = manager.get(parsed_query)

    if len(deleted_objects) == 0:
        click.echo("No object is matching to the specified query.")
        return

    cascade_details = [
        detail for detail in manager.resolve_cascade(deleted_objects)
        if len(detail.not_none_objects()) > 0
    ]

    for detail in cascade_details:
        click.echo(f"\n{detail}")

    if not click.confirm("\nConfirm affected row ?"):
        raise click.Abort()

    try:
        manager.delete(whereclause=parsed_query)

    except IntegrityError as e:
        print(e.__cause__)
        return

    generic_read(manager=manager, model=model, query=None)


__HELP_MESSAGE = "Retreive {model} from a custom query."


# DELETE EMPLOYEES
@delete.command()
@click.option(
    "--query",
    help=__HELP_MESSAGE.format(model="employees"),
    required=True
)
def employees(query):
    """
    Delete on or several employees

    Permissions required = [ACCOUNTING]
    """
    with create_session() as session:
        generic_delete(
            manager=EmployeeManager(session),
            model=Employee,
            query=query
        )


# DELETE CLIENTS
@delete.command()
@click.option(
    "--query",
    help=__HELP_MESSAGE.format(model="clients"),
    required=True
)
def clients(query):
    """
    Delete on or several clients

    Permissions required = [SALES]
    """
    with create_session() as session:
        generic_delete(
            manager=ClientsManager(session),
            model=Client,
            query=query
        )


# DELETE CONTRACTS
@delete.command()
@click.option(
    "--query",
    help=__HELP_MESSAGE.format(model="contracts"),
    required=True
)
def contracts(query):
    """
    Delete on or several contracts

    Permissions required = [ACCOUNTING | SALES]
    """
    with create_session() as session:
        generic_delete(
            manager=ContractsManager(session),
            model=Contract,
            query=query
        )


# DELETE EVENTS
@delete.command()
@click.option(
    "--query",
    help=__HELP_MESSAGE.format(model="events"),
    required=True
)
def events(query):
    """
    Delete on or several events

    Permissions required = [ACCOUNTING | SUPPORT]
    """
    with create_session() as session:
        generic_delete(
            manager=EventsManager(session),
            model=Event,
            query=query
        )
