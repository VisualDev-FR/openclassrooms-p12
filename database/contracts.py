import typing
from sqlalchemy.orm import Session
from database.manager import Manager
from models.contracts import Contract
from models.employees import Department
from authentification.decorators import login_required, permission_required


class EventsManager(Manager):
    """
    Manage the access to ``Contract`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Contract)

    @permission_required(roles=[Department.ACCOUNTING])
    def create(
        total_amount: float,
        client_id: int,
        account_contact_id: int,
        to_be_paid: float = None,
        is_signed: bool = False,
    ) -> Contract:
        contract = Contract(
            total_amount=total_amount,
            client_id=client_id,
            account_contact_id=account_contact_id,
            to_be_paid=to_be_paid or total_amount,
            is_signed=is_signed,
        )

        return super().create(contract)

    @login_required
    def get(self, where_clause) -> typing.List[Contract]:
        return super().get(where_clause)

    @login_required
    def all(self) -> typing.List[Contract]:
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(*args, **kwargs):
        return super().delete(**kwargs)
