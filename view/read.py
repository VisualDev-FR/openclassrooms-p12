from view import cli


@cli.group()
def read():
    """
    Read an existing entry.
    """
    pass


@read.command()
def employee():
    """
    Retreive existing employee
    """
    pass
