import click

from view import cli
from database.employees import EmployeeManager, Employee
from database.clients import ClientsManager, Client
from database.contracts import ContractsManager, Contract
from database.events import EventsManager, Event
from database.manager import create_session, Manager


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

    click.echo(manager.tabulate(objects=objects, headers=manager._model.HEADERS))


__HELP_MESSAGE = (
    "Retreive {model} from a custom query. If not specified, retreive all existing entries."
)


@read.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="employees"))
def employees(query):
    """
    Retreive existing employee
    """
    with create_session() as session:
        generic_read(manager=EmployeeManager(session), model=Employee, query=query)


@read.command()
@click.option(
    "--query", help=__HELP_MESSAGE.format(model="clients")
)
def clients(query):
    """
    Retreive existing clients
    """
    with create_session() as session:
        generic_read(manager=ClientsManager(session), model=Client, query=query)


@read.command()
@click.option(
    "--query", help=__HELP_MESSAGE.format(model="contracts")
)
def contracts(query):
    """
    Retreive existing contracts
    """
    with create_session() as session:
        generic_read(manager=ContractsManager(session), model=Contract, query=query)


@read.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="events"))
def events(query):
    """
    Retreive existing events
    """
    with create_session() as session:
        generic_read(manager=EventsManager(session), model=Event, query=query)
