import sqlalchemy
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from abc import ABC, abstractmethod
from sentry_sdk import capture_message

from controller import authentification as auth
from controller.permissions import permission_required
from controller.cascade import CascadeDetails, CascadeResolver
from controller import utils
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
        self.cascade_resolver = CascadeResolver(session)

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
        self._session.execute(
            sqlalchemy.delete(self._model)
            .where(whereclause)
        )
        self._session.commit()

    @abstractmethod
    def resolve_cascade(self, objects: List[object]) -> List[CascadeDetails]:
        pass


class EmployeeManager(Manager):
    """
    Manage the access to ``Employee`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Employee)

    @permission_required(roles=Department)
    def get(self, *args, **kwargs) -> List[Employee]:
        return super().get(*args, **kwargs)

    @permission_required(roles=Department)
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
                message=f"user {auth.get_authenticated_user_id()} : create employee {created_employee.id}",
            )

        return created_employee

    @permission_required(roles=[Department.ACCOUNTING])
    def update(self, where_clause, **values):

        if "email" in values:
            values["email"] = utils.validate_email(values["email"])

        if "password" in values:
            password = values.pop("password")
            hash, salt = auth.encrypt_password(password)
            values["password_hash"] = hash
            values["salt"] = salt

        super().update(where_clause, **values)

        request = sqlalchemy.select(Employee).where(where_clause)
        updated_employees = self._session.scalars(request)

        capture_message(
            message=f"user {auth.get_authenticated_user_id()} : update employees : {[employee.id for employee in updated_employees]}",
        )

    @permission_required(roles=[Department.ACCOUNTING])
    def delete(self, whereclause):
        return super().delete(whereclause)

    def resolve_cascade(self, employees: List[Employee]) -> List[CascadeDetails]:
        return self.cascade_resolver.resolve_employee_cascade(
            employees=employees
        )


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
    ) -> Client:
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            enterprise=enterprise,
            sales_contact_id=auth.get_authenticated_user_id(),
        )

        return super().create(client)

    @permission_required(roles=Department)
    def get(self, where_clause) -> List[Client]:
        return super().get(where_clause)

    @permission_required(roles=Department)
    def all(self) -> List[Client]:
        return super().all()

    @permission_required(roles=[Department.SALES])
    def update(self, where_clause, **values):

        if "sales_contact_id" in values:
            sales_contact = self._session.scalar(
                sqlalchemy.select(Employee)
                .where(Employee.id == values["sales_contact_id"])
            )

            if sales_contact.department != Department.SALES:
                raise ValueError("sales_contact_id must be a sales employee")

        return super().update(where_clause, **values)

    @permission_required(roles=[Department.SALES])
    def delete(self, whereclause):
        return super().delete(whereclause)

    def filter_by_name(self, name_contains: str):
        return self.get(Client.full_name.contains(name_contains))

    def resolve_cascade(self, clients: List[Client]) -> List[CascadeDetails]:
        return self.cascade_resolver.resolve_clients_cascade(
            clients=clients
        )


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
                account_contact_id=auth.get_authenticated_user_id(),
                total_amount=total_amount,
                to_be_paid=to_be_paid,
                is_signed=is_signed,
            )
        )

    @permission_required(roles=Department)
    def get(self, where_clause) -> List[Contract]:
        return super().get(where_clause)

    @permission_required(roles=Department)
    def all(self) -> List[Contract]:
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def update(self, where_clause, **values):
        return super().update(where_clause, **values)

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def delete(self, whereclause):
        return super().delete(whereclause)

    def resolve_cascade(self, contracts: List[Contract]) -> List[CascadeDetails]:
        return self.cascade_resolver.resolve_contracts_cascade(
            contracts=contracts
        )


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

        support_employee = self._session.scalar(
            sqlalchemy.select(Employee)
            .where(Employee.id == support_contact_id)
        )

        if support_employee.department != Department.SUPPORT:
            raise ValueError(
                "The support_contact_id must be a support Employee."
            )

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

    @permission_required(roles=Department)
    def get(self, where_clause) -> List[Event]:
        return super().get(where_clause)

    @permission_required(roles=Department)
    def all(self) -> List[Event]:
        return super().all()

    @permission_required([Department.ACCOUNTING, Department.SUPPORT])
    def update(self, where_clause, **values):

        user = auth.retreive_authenticated_user(self._session)
        accessed_objects = self.get(where_clause)

        # check that support employee own the accessed events
        if user.department == Department.SUPPORT:
            for event in accessed_objects:
                if event.support_contact_id != user.id:
                    raise PermissionError(
                        f"Permission denied. Not authorized to update event {event.id}"
                    )

        # Chech that support_contact is a support employee
        if "support_contact_id" in values:
            support_contact = self._session.scalar(
                sqlalchemy.select(Employee)
                .where(Employee.id == values["support_contact_id"])
            )

            if support_contact.department != Department.SUPPORT:
                raise ValueError(
                    "support_contact_id must be a support employee"
                )

        return super().update(where_clause, **values)

    @permission_required([Department.ACCOUNTING, Department.SUPPORT])
    def delete(self, where_clause):

        user = auth.retreive_authenticated_user(self._session)
        accessed_objects = self.get(where_clause)

        # check that support employee own the accessed events
        if user.department == Department.SUPPORT:
            for event in accessed_objects:
                if event.support_contact_id != user.id:
                    raise PermissionError(
                        f"Permission denied. Not authorized to update event {event.id}"
                    )

        return super().delete(where_clause)

    def resolve_cascade(self, events: List[Event]) -> List[CascadeDetails]:
        return [
            CascadeDetails(
                title="EVENTS",
                headers=Event.HEADERS,
                objects=events
            )
        ]
