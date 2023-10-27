import click
from datetime import datetime


@click.group()
def cli():
    pass


@cli.group()
def create():
    """
    Create a new entry.
    """
    pass


@cli.group()
def read():
    """
    Read an existing entry.
    """
    pass


@cli.group()
def update():
    """
    Update an existing entry.
    """
    pass


@cli.group()
def delete():
    """
    Delete an existing entry.
    """
    pass


# CREATE EMPLOYEE
@create.command()
@click.option("--email", help="The email of the employee", required=True)
@click.option("--password", help="The password of the employee", required=True)
@click.option(
    "--fullname",
    help="The full name of the employee. sample : 'FirstName, LastName'",
    required=True,
)
@click.option(
    "--department",
    help="The department of the employee",
    type=click.Choice(["sales", "accounting", "support"]),
    required=True,
)
def employee(email, password, fullname, department):
    """
    Create a new employee
    """
    click.echo(locals())


# CREATE CLIENT
@create.command()
@click.option("--email", help="The email of the client", required=True)
@click.option("--fullname", help="The full name of the client", required=True)
@click.option(
    "--sales_contact",
    help="The id of the client's sales contact",
    required=True,
    type=int,
)
@click.option("--phone", help="The phone number of the client")
@click.option("--enterprise", help="The enterprise of the client")
def client(email, fullname, sales_contact, phone, enterprise):
    """
    Create a new client
    """
    click.echo(locals())


# CREATE CONTRACT
@create.command()
@click.option("--client_id", help="The id of the attached client")
@click.option(
    "--account_id",
    help="The id of the accounting employee, managing this contract",
    type=int,
)
@click.option("--total", help="The total amount of the contract", type=float)
@click.option(
    "--to_be_paid", help="The remaing amount of the contract to be paid", type=float
)
@click.option("--signed", help="1 if the contract is signed, else 0", type=bool)
def contract(client_id, account_id, total, to_be_paid, signed):
    """
    Create a new contract
    """
    click.echo(locals())


# CREATE EVENT
@create.command()
@click.option(
    "--start",
    help="The start date of the event",
    type=click.DateTime(formats=[r"%Y-%m-%d", r"%Y/%m/%d"]),
    required=True,
)
@click.option(
    "--end",
    help="The end date of the event",
    type=click.DateTime(formats=[r"%Y-%m-%d", r"%Y/%m/%d"]),
    required=True,
)
@click.option("--location", help="The location of the event", required=True)
@click.option("--attendees", help="The total amount of attendees", required=True)
@click.option(
    "--contract", help="The id of the event's contract", type=int, required=True
)
@click.option(
    "--support",
    help="the id of the support employee, managing this event.",
    type=int,
    required=True,
)
@click.option("--notes", help="Notes about the event")
def event(start, end, location, attendees, contract, support, notes):
    """
    Create a new event
    """
    click.echo(locals())


if __name__ == "__main__":
    cli()
