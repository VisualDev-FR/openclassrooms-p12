import sqlalchemy
from sqlalchemy.orm import Session
from datetime import datetime
from tabulate import tabulate
from typing import List, Any
from abc import ABC
from sentry_sdk import capture_message

from controller.authentification import get_authenticated_user_id
from controller.permissions import login_required, permission_required
from models.employees import Department, Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event


class Manager(ABC):
    """
    class template to implement model managers.

    A model manager shall implement all CRUD methods to access or modify datas.
    """

    def __init__(self, session: Session, model: type) -> None:
        self._session = session
        self._model = model

    def create(self, obj):
        self._session.add(obj)
        self._session.commit()

        return obj

    def all(self):
        request = sqlalchemy.select(self._model)
        return self._session.scalars(request).all()

    def get(self, where_clause):
        request = sqlalchemy.select(self._model).where(where_clause)
        return self._session.scalars(request).all()

    def update(self, where_clause, **values):
        self._session.execute(
            sqlalchemy.update(self._model).where(where_clause).values(**values)
        )
        self._session.commit()

    def delete(self, whereclause):
        self._session.execute(sqlalchemy.delete(
            self._model).where(whereclause))
        self._session.commit()

    def tabulate(self, objects: List[Any], headers: List[str]) -> str:
        """
        Prettify a list of objects to a tabulated view.

        Args:
        * ``objects``: a list of objects to display, the objects must implement the method ``to_list()``
        * ``headers``: a list of strings containing the headers of the tabulated view

        Returns:
        A string representing the table of the given datas

        """
        return "\n" + tabulate(
            tabular_data=[obj.to_list() for obj in objects], headers=headers
        ) + "\n"


class EmployeeManager(Manager):
    """
    Manage the access to ``Employee`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Employee)

    @login_required
    def get(self, *args, **kwargs) -> List[Employee]:
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> List[Employee]:
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING])
    def create(self, full_name: str, email: str, password: str, department: Department):
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=department,
        )

        new_employee.set_password(password)

        created_employee = super().create(new_employee)

        if created_employee is not None:
            capture_message(
                message=f"user {get_authenticated_user_id()} : create employee {created_employee.id}",
            )

        return created_employee

    @permission_required(roles=[Department.ACCOUNTING])
    def update(self, where_clause, **values):
        super().update(where_clause, **values)

        request = sqlalchemy.select(Employee).where(where_clause)
        updated_employees = self._session.scalars(request)

        capture_message(
            message=f"user {get_authenticated_user_id()} : update employees : {[employee.id for employee in updated_employees]}",
        )

    @permission_required(roles=[Department.ACCOUNTING])
    def delete(self, whereclause):
        return super().delete(whereclause)


class ClientsManager(Manager):
    """
    Manage the access to ``Client`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Client)

    @permission_required(roles=[Department.SALES])
    def create(
        self,
        email: str,
        full_name: str,
        phone: str,
        enterprise: str,
        sales_contact_id: int,
    ) -> Client:
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            enterprise=enterprise,
            sales_contact_id=sales_contact_id,
        )

        return super().create(client)

    @login_required
    def get(self, *args, **kwargs) -> List[Client]:
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> List[Client]:
        return super().all()

    @permission_required(roles=[Department.SALES])
    def update(self, where_clause, **values):
        return super().update(where_clause, **values)

    @permission_required(roles=[Department.SALES])
    def delete(self, whereclause):
        return super().delete(whereclause)

    def filter_by_name(self, name_contains: str):
        return self.get(Client.full_name.contains(name_contains))


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
    def get(self, where_clause) -> List[Contract]:
        return super().get(where_clause)

    @login_required
    def all(self) -> List[Contract]:
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def update(self, where_clause, **values):
        return super().update(where_clause, **values)

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def delete(self, whereclause):
        return super().delete(whereclause)


class EventsManager(Manager):
    """
    Manage the access to ``Event`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Event)

    @permission_required([Department.SALES])
    def create(
        self,
        start_date=datetime,
        end_date=datetime,
        location=str,
        attendees_count=int,
        notes=str,
        contract_id=int,
        support_contact_id=int,
    ):
        return super().create(
            Event(
                start_date=start_date,
                end_date=end_date,
                location=location,
                attendees_count=attendees_count,
                notes=notes,
                contract_id=contract_id,
                support_contact_id=support_contact_id,
            )
        )

    @login_required
    def get(self, *args, **kwargs) -> List[Event]:
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> List[Event]:
        return super().all()

    @permission_required([Department.ACCOUNTING, Department.SUPPORT])
    def update(self, where_clause, **values):
        return super().update(where_clause, **values)

    @permission_required([Department.ACCOUNTING, Department.SUPPORT])
    def delete(self, whereclause):
        return super().delete(whereclause)
