import typing
from sqlalchemy.orm import Session
from database.manager import Manager
from models.contracts import Contract
from models.employees import Department
from authentification.decorators import login_required, permission_required
from authentification.token import get_authenticated_user_id


class ContractsManager(Manager):
    """
    Manage the access to ``Contract`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Contract)

    @permission_required(roles=[Department.ACCOUNTING])
    def create(
        self, client_id: int, total_amount: float, to_be_paid: int, is_signed: bool
    ):
        return super().create(
            Contract(
                client_id=client_id,
                account_contact_id=get_authenticated_user_id(),
                total_amount=total_amount,
                to_be_paid=to_be_paid,
                is_signed=is_signed,
            )
        )

    @login_required
    def get(self, where_clause) -> typing.List[Contract]:
        return super().get(where_clause)

    @login_required
    def all(self) -> typing.List[Contract]:
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def update(self, where_clause, **values):
        return super().update(where_clause, **values)

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def delete(self, whereclause):
        return super().delete(whereclause)
