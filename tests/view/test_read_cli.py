from click.testing import CliRunner

from view.read import employees, clients, contracts, events
from conftest import login_as_accounting


def test_read_client(database_mock):

    with database_mock, login_as_accounting():
        runner = CliRunner()
        result = runner.invoke(cli=employees)

        stdout = result.output

        assert "sales.employee@epicevents.co" in stdout
        assert "account.employee@epicevents.co" in stdout
        assert "support.employee@epicevents.co" in stdout