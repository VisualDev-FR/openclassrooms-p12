import click
from sqlalchemy.exc import IntegrityError

from view import cli
from view.read import generic_read
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event
from controller import utils
from controller import database as db
from controller.managers import (
    Manager,
    EmployeeManager,
    ClientsManager,
    ContractsManager,
    EventsManager,
)


@cli.group()
def update():
    """
    Update an existing entry.
    """
    pass


def generic_update(manager: Manager, model: type, query: str, **kwargs):
    """
    Generic function to update datas.

    Args:
    * ``manager``: the manager of the updated model
    * ``model``: the model of the updated data
    * ``kwargs``: the parameters to be updated
    """

    params = utils.drop_dict_none_values(kwargs)

    if len(params) == 0:
        click.echo("No parameters were specified.")
        raise click.Abort()

    try:
        full_query = f"{model.__name__}.{query}"
        parsed_query = eval(full_query)

    except (NameError, AttributeError, SyntaxError):
        click.echo(f"query error: {full_query}")
        return

    generic_read(manager=manager, model=model, query=query)

    if not click.confirm("Confirm affected rows ?"):
        raise click.Abort()

    try:
        manager.update(where_clause=parsed_query, **params)

    except IntegrityError as e:
        print(e.__cause__)
        return

    generic_read(manager=manager, model=model, query=query)


# UPDATE EMPLOYEES
@update.command()
@click.option(
    "--query",
    help="A query to select entries to update",
    required=True
)
@click.option(
    "--email",
    help="The email of the employee"
)
@click.option(
    "--password",
    help="The password of the employee",
)
@click.option(
    "--fullname",
    help="The full name of the employee. sample : 'FirstName, LastName'",
)
@click.option(
    "--department",
    help="The department of the employee",
    type=click.Choice(["sales", "accounting", "support"]),
)
def employees(query, email, password, fullname, department):
    """
    Update one or several existing employees.
    """
    with db.create_session() as session:
        generic_update(
            manager=EmployeeManager(session),
            model=Employee,
            query=query,
            email=email,
            password=password,
            full_name=fullname,
            department=department,
        )


# UPDATE CLIENTS
@update.command()
@click.option(
    "--query",
    help="A query to select entries to update",
    required=True
)
@click.option(
    "--email",
    help="The email of the client"
)
@click.option(
    "--fullname",
    help="The full name of the client"
)
@click.option(
    "--sales_contact",
    help="The id of the client's sales contact",
    type=int,
)
@click.option(
    "--phone",
    help="The phone number of the client"
)
@click.option(
    "--enterprise",
    help="The enterprise of the client"
)
def clients(query, email, fullname, sales_contact, phone, enterprise):
    """
    Update one or several existing clients.

    Permissions requrired = [SALES]
    """
    with db.create_session() as session:
        generic_update(
            manager=ClientsManager(session),
            model=Client,
            query=query,
            email=email,
            full_name=fullname,
            sales_contact_id=sales_contact,
            phone=phone,
            enterprise=enterprise,
        )


# UPDATE CONTRACTS
@update.command()
@click.option(
    "--query",
    help="A query to select entries to update",
    required=True
)
@click.option(
    "--client_id",
    help="The id of the attached client"
)
@click.option(
    "--account_id",
    help="The id of accounting employee in charge of this contract."
)
@click.option(
    "--total",
    help="The total amount of the contract",
    type=float
)
@click.option(
    "--to_be_paid",
    help="The remaing amount of the contract to be paid",
    type=float,
)
@click.option(
    "--signed",
    help="1 if the contract is signed, else 0",
    type=bool
)
def contracts(query, client_id, account_id, total, to_be_paid, signed):
    """
    Update one or several existing contracts.
    """
    with db.create_session() as session:
        generic_update(
            manager=ContractsManager(session),
            model=Contract,
            query=query,
            client_id=client_id,
            account_contact_id=account_id,
            total_amount=total,
            to_be_paid=to_be_paid,
            is_signed=signed,
        )


# UPDATE EVENT
@update.command()
@click.option(
    "--query",
    help="A query to select entries to update",
    required=True
)
@click.option(
    "--start",
    help="The start date of the event",
    type=click.DateTime(formats=[r"%Y-%m-%d", r"%Y/%m/%d"]),
)
@click.option(
    "--end",
    help="The end date of the event",
    type=click.DateTime(formats=[r"%Y-%m-%d", r"%Y/%m/%d"]),
)
@click.option(
    "--location",
    help="The location of the event",
)
@click.option(
    "--attendees",
    help="The total amount of attendees",
)
@click.option(
    "--contract_id",
    help="The id of the event's contract",
    type=int,
)
@click.option(
    "--support_id",
    help="the id of the support employee, managing this event.",
    type=int,
)
@click.option(
    "--notes",
    help="Notes about the event"
)
def events(
    query,
    start,
    end,
    location,
    attendees,
    contract_id,
    support_id,
    notes
):
    """
    Update one or several existing events.
    """
    with db.create_session() as session:
        generic_update(
            manager=EventsManager(session),
            model=Event,
            query=query,
            start_date=start,
            end_date=end,
            location=location,
            attendees_count=attendees,
            notes=notes,
            contract_id=contract_id,
            support_contact_id=support_id,
        )
