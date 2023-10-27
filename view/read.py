import click

from view import cli
from database.employees import EmployeeManager
from database.manager import create_session
from models.employees import Employee


@cli.group()
def read():
    """
    Read an existing entry.
    """
    pass


@read.command()
@click.option("--id", help="Retreive an employee from his id")
def employee(id):
    """
    Retreive existing employee
    """
    with create_session() as session:

        manager = EmployeeManager(session)

        if id is not None:

            employee = manager.get(Employee.id == id)

            click.echo(employee[0].full_name)
