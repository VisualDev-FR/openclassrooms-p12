import sqlalchemy
from sqlalchemy.orm import Session
from click.testing import CliRunner

from models.employees import Employee, Department
from models.clients import Client
from models.contracts import Contract
from models.events import Event
from view.delete import generic_delete
from view import cli


def test_generic_delete():
    # TODO: test_generic_delete
    pass


def count_objects(model: type, session: Session):
    return len(session.scalars(sqlalchemy.select(model)).all())


def test_delete_employee(database_mock, session: Session, login_as_sales, force_click_confirm):

    with database_mock, login_as_sales, force_click_confirm:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "delete", "employees",
            "--query", "id==1",
        ])

        print("\n", result.output)

        assert "EMPLOYEES" in result.output
        assert "CLIENTS" in result.output
        assert "CONTRACTS" in result.output
        assert "EVENTS" in result.output


def test_delete_clients(database_mock, session: Session, login_as_sales, force_click_confirm):

    with database_mock, login_as_sales, force_click_confirm:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "delete", "clients",
            "--query", "id==1",
        ])

        print("\n", result.output)

        assert count_objects(Client, session) == 9

        assert "CLIENTS" in result.output
        assert "CONTRACTS" in result.output
        assert "EVENTS" in result.output


def test_delete_contract(database_mock, session: Session, login_as_sales, force_click_confirm):

    with database_mock, login_as_sales, force_click_confirm:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "delete", "contracts",
            "--query", "id==1",
        ])

        print("\n", result.output)

        assert count_objects(Contract, session) == 9

        assert "CONTRACTS" in result.output
        assert "EVENTS" in result.output


def test_delete_event(database_mock, session: Session, login_as_sales, force_click_confirm):

    with database_mock, login_as_sales, force_click_confirm:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "delete", "events",
            "--query", "id==1",
        ])

        print("\n", result.output)

        assert "EVENTS" in result.output
