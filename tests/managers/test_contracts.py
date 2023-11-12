import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from controller.managers import ContractsManager
from models.contracts import Contract
from models.events import Event


DUMMY_CONTRACT = {
    "total_amount": 9499.99,
    "to_be_paid": 9499.99,
    "is_signed": False,
    "client_id": 1,
}


def test_create_contract_from_accounting_employee(session, login_as_accounting):
    """
    Check that accounting employees are allowed to create a new client
    """

    manager = ContractsManager(session)

    with login_as_accounting:
        created_contract = manager.create(**DUMMY_CONTRACT)
        assert created_contract is not None


def test_create_contract_from_unauthorized(session, login_as_sales, login_as_support):
    """
    Check that sales and support employees are not allowed to create a contract
    """
    manager = ContractsManager(session)

    with login_as_sales, pytest.raises(PermissionError):
        created_contract = manager.create(**DUMMY_CONTRACT)
        assert created_contract is None

    with login_as_support, pytest.raises(PermissionError):
        created_contract = manager.create(**DUMMY_CONTRACT)
        assert created_contract is None


def test_get_all_contracts(session, login_as_accounting, login_as_sales, login_as_support):
    """
    Check that all contracts can be accessed from all users.
    """
    manager = ContractsManager(session)

    def get_all_contracts():
        all_contracts = manager.all()
        assert len(all_contracts) == 1

    with login_as_accounting:
        get_all_contracts()

    with login_as_sales:
        get_all_contracts()

    with login_as_support:
        get_all_contracts()


def test_get_contract(session, login_as_accounting, login_as_sales, login_as_support):
    manager = ContractsManager(session)

    def get_contract():
        contract = manager.get(Contract.client_id == 1)
        assert contract[0].total_amount == 99.9

    with login_as_accounting:
        get_contract()

    with login_as_sales:
        get_contract()

    with login_as_support:
        get_contract()


def test_update_contract_from_authorized(session, login_as_accounting, login_as_sales):
    manager = ContractsManager(session)

    def update_contract():
        manager.update(where_clause=Contract.client_id == 1, total_amount=50)

        assert manager.get(Contract.client_id == 1)[0].total_amount == 50

    with login_as_accounting:
        update_contract()

    with login_as_sales:
        update_contract()


def test_update_contract_from_unauthorized(session, login_as_support):
    manager = ContractsManager(session)

    with login_as_support, pytest.raises(PermissionError):
        manager.update(where_clause=Contract.client_id == 1, total_amount=50)


def test_delete_contract(session: Session, login_as_sales):

    manager = ContractsManager(session)

    def count_events() -> int:
        return len(session.scalars(sqlalchemy.select(Event)).all())

    with login_as_sales:

        assert count_events() == 1

        manager.delete(Contract.client_id == 1)

        # check that conctract has been correctly deleted
        assert manager.get(Contract.client_id == 1) == []

        # check that associated events have been deleted
        assert count_events() == 0


def test_delete_contract_from_unothorized(session, login_as_support):
    manager = ContractsManager(session)

    with login_as_support, pytest.raises(PermissionError):
        manager.delete(whereclause=Contract.client_id == 1)
