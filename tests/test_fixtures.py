from tests.conftest import login_as_accounting, login_as_sales, login_as_support
from authentification.token import retreive_token, decode_token
from database.employees import EmployeeManager
from models.employees import Employee, Department


def test_login_fixtures(session):
    """
    Check that all roles login functions have the expected behavior
    """

    # login as accounting user
    with login_as_accounting(session):
        token = retreive_token()
        payload = decode_token(token)

        authenticated_user_id = payload["user_id"]

        manager = EmployeeManager(session)

        assert (
            manager.get(Employee.id == authenticated_user_id)[0].department
            == Department.ACCOUNTING
        )

    assert retreive_token() is None

    # login as sales
    with login_as_sales(session):
        token = retreive_token()
        payload = decode_token(token)

        authenticated_user_id = payload["user_id"]

        manager = EmployeeManager(session)

        assert (
            manager.get(Employee.id == authenticated_user_id)[0].department
            == Department.SALES
        )

    assert retreive_token() is None

    # login as support
    with login_as_support(session):
        token = retreive_token()
        payload = decode_token(token)

        authenticated_user_id = payload["user_id"]

        manager = EmployeeManager(session)

        assert (
            manager.get(Employee.id == authenticated_user_id)[0].department
            == Department.SUPPORT
        )

    assert retreive_token() is None
