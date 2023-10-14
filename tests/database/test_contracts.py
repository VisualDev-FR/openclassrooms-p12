import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from database.contracts import ContractsManager
from models.contracts import Contract
from tests.conftest import login_as_accounting, login_as_sales, login_as_support


DUMMY_CONTRACT = {
    "total_amount": 9499.99,
    "to_be_paid": 9499.99,
    "is_signed": False,
    "client_id": 1,
}


def test_create_contract_from_accounting_employee(session):
    """
    Check that accounting employees are allowed to create a new client
    """

    manager = ContractsManager(session)

    with login_as_accounting():
        created_contract = manager.create(**DUMMY_CONTRACT)
        assert created_contract is not None


def test_create_contract_from_unauthorized(session):
    """
    Check that sales and support employees are not allowed to create a contract
    """
    manager = ContractsManager(session)

    with login_as_sales(), pytest.raises(PermissionError):
        created_contract = manager.create(**DUMMY_CONTRACT)
        assert created_contract is None

    with login_as_support(), pytest.raises(PermissionError):
        created_contract = manager.create(**DUMMY_CONTRACT)
        assert created_contract is None
