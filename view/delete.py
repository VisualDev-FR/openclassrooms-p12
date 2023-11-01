import click
from sqlalchemy.exc import IntegrityError

from view import cli
from view.read import generic_read
from database.employees import EmployeeManager, Employee
from database.clients import ClientsManager, Client
from database.contracts import ContractsManager, Contract
from database.events import EventsManager, Event
from database.manager import create_session, Manager


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

    generic_read(manager=manager, model=model, query=query)

    if not click.confirm("Confirm affected row ?"):
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
@click.option("--query", help=__HELP_MESSAGE.format(model="employees"), required=True)
def employees(query):
    """
    Delete on or several employees
    """
    with create_session() as session:
        generic_delete(manager=EmployeeManager(session), model=Employee, query=query)


# DELETE CLIENTS
@delete.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="clients"), required=True)
def clients(query):
    """
    Delete on or several clients
    """
    with create_session() as session:
        generic_delete(manager=ClientsManager(session), model=Client, query=query)


# DELETE CONTRACTS
@delete.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="contracts"), required=True)
def contracts(query):
    """
    Delete on or several contracts
    """
    with create_session() as session:
        generic_delete(manager=ContractsManager(session), model=Contract, query=query)


# DELETE EVENTS
@delete.command()
@click.option("--query", help=__HELP_MESSAGE.format(model="events"), required=True)
def events(query):
    """
    Delete on or several events
    """
    with create_session() as session:
        generic_delete(manager=EventsManager(session), model=Event, query=query)
