import sqlalchemy
from sqlalchemy.orm import Session
from typing import List, Any

from controller import utils
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event


class CascadeDetails:
    """
    Data object storing deletion cascade details.
    """

    def __init__(self, title: str, headers: List[str], objects: List[Any]) -> None:
        self.title = title
        self.objects = objects
        self.headers = headers

    def __str__(self):
        return "\n".join([
            self.title,
            utils.tabulate(
                objects=self.objects,
                headers=self.headers
            )
        ])

    def __repr__(self) -> str:
        return self.__str__()


class CascadeResolver:
    """
    Wrapper handling the logical of deletion cascades retreiving
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def _retreive_clients_from_employees(self, employees: List[Employee]) -> List[Client]:
        return [
            self.session.scalar(
                sqlalchemy.select(Client)
                .where(Client.sales_contact_id == employee.id)
            )
            for employee in employees
        ]

    def _retreive_contracts_from_employees(self, employees: List[Employee]) -> List[Contract]:
        return [
            self.session.scalar(
                sqlalchemy.select(Contract)
                .where(Contract.account_contact_id == employee.id)
            )
            for employee in employees
        ]

    def _retreive_events_from_employee(self, employees: List[Employee]) -> List[Event]:
        return [
            self.session.scalar(
                sqlalchemy.select(Event)
                .where(Event.support_contact_id == employee.id)
            )
            for employee in employees
        ]

    def _retreive_contracts_from_clients(self, clients: List[Client]) -> List[Contract]:
        return [
            self.session.scalar(
                sqlalchemy.select(Contract)
                .where(Contract.client_id == client.id)
            )
            for client in clients
        ]

    def _retreive_events_from_contracts(self, contracts: List[Contract]) -> List[Event]:
        return [
            self.session.scalar(
                sqlalchemy.select(Event)
                .where(Event.contract_id == contract.id)
            )
            for contract in contracts
        ]

    def resolve_employee_cascade(self, employees: List[Employee]) -> List[CascadeDetails]:

        clients = self._retreive_clients_from_employees(employees)

        contracts = (
            self._retreive_contracts_from_employees(employees)
            + self._retreive_contracts_from_clients(clients)
        )

        events = (
            self._retreive_events_from_employee(employees)
            + self._retreive_events_from_contracts(contracts)
        )

        return [
            CascadeDetails(
                title="EMPLOYEES",
                headers=Employee.HEADERS,
                objects=employees,
            ),
            CascadeDetails(
                title="CLIENTS",
                headers=Client.HEADERS,
                objects=clients,
            ),
            CascadeDetails(
                title="CONTRACTS",
                headers=Contract.HEADERS,
                objects=contracts,
            ),
            CascadeDetails(
                title="EVENTS",
                headers=Event.HEADERS,
                objects=events
            )
        ]

    def resolve_clients_cascade(self, clients: List[Client]) -> List[CascadeDetails]:

        contracts = self._retreive_contracts_from_clients(clients)
        events = self._retreive_events_from_contracts(contracts)

        return [
            CascadeDetails(
                title="CLIENTS",
                headers=Client.HEADERS,
                objects=clients,
            ),
            CascadeDetails(
                title="CONTRACTS",
                headers=Contract.HEADERS,
                objects=contracts
            ),
            CascadeDetails(
                title="EVENTS",
                headers=Event.HEADERS,
                objects=events
            )
        ]

    def resolve_contracts_cascade(self, contracts: List[Contract]) -> List[CascadeDetails]:

        events = self._retreive_events_from_contracts(contracts)

        return [
            CascadeDetails(
                title="CONTRACTS",
                headers=Contract.HEADERS,
                objects=contracts,
            ),
            CascadeDetails(
                title="EVENTS",
                headers=Event.HEADERS,
                objects=events,
            )
        ]
