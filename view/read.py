import click

from view import cli
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event
from controller import database as db
from controller.managers import (
    Manager,
    EmployeeManager,
    ClientsManager,
    ContractsManager,
    EventsManager,
)


@cli.group()
def read():
    """
    Read an existing entry.
    """
    pass


def generic_read(manager: Manager, model: type, query: str):
    """
    Generic view to retreive datas and display them in a tabulated view.

    Args:
    * ``manager``: the manager of the accessed datas
    * ``model``: the model of the accessed datas
    * ``query``: a string containing a query to apply on the given manager
    """
    if query is None:
        objects = manager.all()

    else:
        try:
            full_query = f"{model.__name__}.{query}"
            objects = manager.get(eval(full_query))

        except (NameError, AttributeError, SyntaxError):
            click.echo(f"query error: {full_query}")
            return

    click.echo(
        manager.tabulate(objects=objects, headers=manager._model.HEADERS)
    )


__HELP_MESSAGE = "Retreive {model} from a custom query. If not specified, retreive all existing entries."


# READ EMPLOYEES
@read.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="employees"))
def employees(query):
    """
    Retreive existing employee
    """
    with db.create_session() as session:
        generic_read(
            manager=EmployeeManager(session),
            model=Employee,
            query=query
        )


# READ CLIENTS
@read.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="clients"))
def clients(query):
    """
    Retreive existing clients
    """
    with db.create_session() as session:
        generic_read(
            manager=ClientsManager(session),
            model=Client,
            query=query
        )


# READ CONTRACTS
@read.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="contracts"))
def contracts(query):
    """
    Retreive existing contracts
    """
    with db.create_session() as session:
        generic_read(
            manager=ContractsManager(session),
            model=Contract,
            query=query
        )


# READ EVENTS
@read.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="events"))
def events(query):
    """
    Retreive existing events
    """
    with db.create_session() as session:
        generic_read(
            manager=EventsManager(session),
            model=Event,
            query=query
        )
