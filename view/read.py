import click

from view import cli
from database.employees import EmployeeManager, Employee
from database.clients import ClientsManager, Client
from database.contracts import ContractsManager, Contract
from database.events import EventsManager, Event
from database.manager import create_session, Manager
from tabulate import tabulate


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
    * ``all``: a boolean indacating if all the datas needs to be retreived
    * ``query``: a string containing a query to apply on the given manager
    """
    if query is None:
        objects = manager.all()

    else:
        try:
            full_query = f"{model.__name__}.{query}"
            objects = manager.get(eval(full_query))

        except (NameError, AttributeError):
            click.echo(f"query error: {full_query}")
            return

    click.echo(manager.tabulate(objects=objects, headers=manager._model.HEADERS))


@read.command()
@click.option(
    "--query", help="Retreive employees from a custom query. Sample : 'id == 5'"
)
def employees(query):
    """
    Retreive existing employee
    """
    with create_session() as session:
        generic_read(manager=EmployeeManager(session), model=Employee, query=query)


@read.command()
@click.option(
    "--query", help="Retreive clients from a custom query. Sample : 'id == 5'"
)
def clients(query):
    """
    Retreive existing clients
    """
    with create_session() as session:
        generic_read(manager=ClientsManager(session), model=Client, query=query)


@read.command()
@click.option(
    "--query", help="Retreive contracts from a custom query. Sample : 'id == 5'"
)
def contracts(query):
    with create_session() as session:
        generic_read(manager=ContractsManager(session), model=Contract, query=query)


@read.command()
@click.option("--query", help="Retreive events from a custom query. Sample : 'id == 5'")
def events(query):
    with create_session() as session:
        generic_read(manager=EventsManager(session), model=Event, query=query)
