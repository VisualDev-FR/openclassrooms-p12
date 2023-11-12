import click
from sqlalchemy.exc import IntegrityError

from view import cli
from controller import utils
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
def create():
    """
    Create a new entry.
    """
    pass


def generic_create(manager: Manager, model: type, **kwargs):
    """
    Generic view to create an object, and display details in a tabulated view.

    Args:
    * ``manager``: the manager of the created model
    * ``model``: the model of the created data
    * ``kwargs``: the attributes of the object to create
    """
    try:
        created_object = manager.create(**kwargs)

    except IntegrityError as e:
        click.echo(f"Integrity error : {e.__cause__}")
        return

    click.echo(
        utils.tabulate(objects=[created_object], headers=model.HEADERS)
    )


# CREATE EMPLOYEE
@create.command()
@click.option(
    "--email",
    prompt=True,
    help="The email of the employee",
    required=True
)
@click.option(
    "--password",
    prompt=True,
    help="The password of the employee",
    required=True,
)
@click.option(
    "--fullname",
    prompt=True,
    help="The full name of the employee. sample : 'FirstName, LastName'",
    required=True,
)
@click.option(
    "--department",
    prompt=True,
    help="The department of the employee",
    type=click.Choice(["sales", "accounting", "support"]),
    required=True,
)
def employees(email, password, fullname, department):
    """
    Create a new employee.

    Permissions required : [ACCOUNTING]
    """
    with db.create_session() as session:
        generic_create(
            manager=EmployeeManager(session),
            model=Employee,
            full_name=fullname,
            email=email,
            password=password,
            department=department,
        )


# CREATE CLIENT
@create.command()
@click.option(
    "--email",
    prompt=True,
    help="The email of the client",
    required=True
)
@click.option(
    "--fullname",
    prompt=True,
    help="The full name of the client",
    required=True
)
@click.option(
    "--sales_contact",
    prompt=True,
    help="The id of the client's sales contact",
    required=True,
    type=int,
)
@click.option(
    "--phone",
    prompt=True,
    help="The phone number of the client"
)
@click.option(
    "--enterprise",
    prompt=True,
    help="The enterprise of the client"
)
def clients(email, fullname, sales_contact, phone, enterprise):
    """
    Create a new client

    Permissions required : [SALES]
    """
    with db.create_session() as session:
        generic_create(
            manager=ClientsManager(session),
            model=Client,
            email=email,
            full_name=fullname,
            sales_contact_id=sales_contact,
            phone=phone,
            enterprise=enterprise,
        )


# CREATE CONTRACT
@create.command()
@click.option(
    "--client_id",
    prompt=True,
    help="The id of the attached client"
)
@click.option(
    "--total",
    prompt=True,
    help="The total amount of the contract",
    type=float
)
@click.option(
    "--to_be_paid",
    prompt=True,
    help="The remaing amount of the contract to be paid",
    type=float,
)
@click.option(
    "--signed",
    prompt=True,
    help="1 if the contract is signed, else 0",
    type=bool
)
def contracts(client_id, total, to_be_paid, signed):
    """
    Create a new contract

    Permissions required : [ACCOUNTING]
    """
    with db.create_session() as session:
        generic_create(
            manager=ContractsManager(session),
            model=Contract,
            client_id=client_id,
            total_amount=total,
            to_be_paid=to_be_paid,
            is_signed=signed,
        )


# CREATE EVENT
@create.command()
@click.option(
    "--start",
    prompt=True,
    help="The start date of the event",
    type=click.DateTime(formats=[r"%Y-%m-%d", r"%Y/%m/%d"]),
    required=True,
)
@click.option(
    "--end",
    prompt=True,
    help="The end date of the event",
    type=click.DateTime(formats=[r"%Y-%m-%d", r"%Y/%m/%d"]),
    required=True,
)
@click.option(
    "--location",
    prompt=True,
    help="The location of the event",
    required=True
)
@click.option(
    "--attendees",
    prompt=True,
    help="The total amount of attendees",
    required=True
)
@click.option(
    "--contract_id",
    prompt=True,
    help="The id of the event's contract",
    type=int,
    required=True,
)
@click.option(
    "--support_id",
    prompt=True,
    help="the id of the support employee, managing this event.",
    type=int,
    required=True,
)
@click.option(
    "--notes",
    prompt=True,
    help="Notes about the event"
)
def events(start, end, location, attendees, contract_id, support_id, notes):
    """
    Create a new event

    Permissions required : [SALES]
    """
    with db.create_session() as session:
        generic_create(
            manager=EventsManager(session),
            model=Event,
            start_date=start,
            end_date=end,
            location=location,
            attendees_count=attendees,
            notes=notes,
            contract_id=contract_id,
            support_contact_id=support_id,
        )
