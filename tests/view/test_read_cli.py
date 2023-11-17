from click.testing import CliRunner

from view.read import (
    employees as read_employees,
    clients as read_clients,
    contracts as read_contracts,
    events as read_events,
)


# READ EMPLOYEES
def test_read_all_employees(database_mock, login_as_accounting):

    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(cli=read_employees)

        stdout = result.output

        assert len(result.output.split("\n")) == 13
        assert "sales.employee@epicevents.co" in stdout
        assert "account.employee@epicevents.co" in stdout
        assert "support.employee@epicevents.co" in stdout


def test_read_some_employees(database_mock, login_as_accounting):

    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(cli=read_employees, args=["--query", "id==1"])
        stdout = result.output

        assert len(result.output.split("\n")) == 4
        assert "sales.employee@epicevents.co" in stdout


# READ CLIENTS
def test_read_all_clients(database_mock, login_as_accounting):

    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(read_clients)

        assert len(result.output.split("\n")) == 13
        assert "alice.johnson@example.com" in result.output
        assert "franklin.lee@example.com" in result.output
        assert "isabella.adams@example.com" in result.output


def test_read_some_clients(database_mock, login_as_accounting):

    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(read_clients, args=["--query", "id==1"])

        assert len(result.output.split("\n")) == 4
        assert "alice.johnson@example.com" in result.output


# READ CONTRACTS
def test_read_all_contracts(database_mock, login_as_accounting):

    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(read_contracts)

        assert len(result.output.split("\n")) == 13
        assert "account_contact_id" in result.output
        assert "to_be_paid" in result.output


def test_read_some_contracts(database_mock, login_as_accounting):

    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(read_contracts, args=["--query", "id==1"])

        assert len(result.output.split("\n")) == 4
        assert "5000" in result.output


# READ EVENTS
def test_read_all_events(database_mock, login_as_accounting):

    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(read_events)

        assert len(result.output.split("\n")) == 13
        assert "Réunion annuelle de l'entreprise" in result.output
        assert "Salon professionnel" in result.output


def test_read_some_events(database_mock, login_as_accounting):
    with database_mock, login_as_accounting:

        runner = CliRunner()
        result = runner.invoke(read_events, args=["--query", "id==1"])

        assert len(result.output.split("\n")) == 4
        assert "Réunion annuelle de l'entreprise" in result.output
