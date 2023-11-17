import click
from sentry_sdk import capture_exception
from view import (
    cli,
    create,
    read,
    update,
    delete,
    login,
    logout,
    signup,
    init_database
)

if __name__ == "__main__":
    try:
        cli()

    except PermissionError as e:
        click.echo(e)

    except ValueError as e:
        click.echo(e)

    except Exception as e:
        # TODO: handle exceptions here
        # capture_exception(e)
        raise e
