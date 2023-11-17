import sqlalchemy
from sqlalchemy.orm import Session
from click.testing import CliRunner

from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event
from view import update
from view import cli


def test_update_employee(database_mock, session: Session, login_as_accounting, force_click_confirm):

    with database_mock, login_as_accounting, force_click_confirm:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "update", "employees",
            "--query", "id==1",
            "--email", "updated.email@example.co"
        ])

        print("\n", result.output)

        updated_object = session.scalar(
            sqlalchemy.select(Employee)
            .where(Employee.id == 1)
        )

        assert updated_object.email == "updated.email@example.co"
        assert "sales.employee@epicevents.co" in result.output
        assert "updated.email@example.co" in result.output


def test_update_client(database_mock, session: Session, login_as_sales, force_click_confirm):

    with database_mock, login_as_sales, force_click_confirm:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "update", "clients",
            "--query", "id==1",
            "--email", "updated.email@example.co"
        ])

        print("\n", result.output)

        updated_object = session.scalar(
            sqlalchemy.select(Client)
            .where(Client.id == 1)
        )

        assert updated_object.email == "updated.email@example.co"
        assert "updated.email@example.co" in result.output
        assert "alice.johnson@example.com" in result.output


def test_update_contract(database_mock, session: Session, login_as_accounting, force_click_confirm):

    with database_mock, login_as_accounting, force_click_confirm:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "update", "contracts",
            "--query", "id==1",
            "--to_be_paid", "0"
        ])

        print("\n", result.output)

        updated_object = session.scalar(
            sqlalchemy.select(Contract)
            .where(Contract.id == 1)
        )

        assert updated_object.to_be_paid == 0


def test_update_event(database_mock, session: Session, login_as_accounting, force_click_confirm):

    with database_mock, login_as_accounting, force_click_confirm:
        runner = CliRunner()
        result = runner.invoke(cli, args=[
            "update", "events",
            "--query", "id==1",
            "--location", "updated location"
        ])

        print("\n", result.output)

        updated_object = session.scalar(
            sqlalchemy.select(Event)
            .where(Event.id == 1)
        )

        assert updated_object.location == "updated location"
        assert "updated location" in result.output
        assert "Salle A" in result.output
