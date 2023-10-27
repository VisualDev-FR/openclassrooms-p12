import click


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
    click.echo(
        f"Creating employee with email {email}, password {password}, name {fullname}, department {department}"
    )


@create.command()
@click.option("--email", help="The email of the client", required=True)
@click.option("--fullname", help="The full name of the client", required=True)
@click.option(
    "--sales_contact",
    help="The id of the client's sales contact",
    required=True,
    type=int,
)
@click.option("--phone", help="The phone of the client")
@click.option("--enterprise", help="The enterprise of the client")
def client(email, fullname, sales_contact, phone, enterprise):
    click.echo(locals())


@create.command()
def contract():
    click.echo(locals())


@create.command()
def event():
    click.echo(locals())


if __name__ == "__main__":
    cli()
