import typing
from sqlalchemy.orm import Session
from database.manager import Manager
from models.clients import Client
from models.employees import Department as roles
from authentification.decorators import login_required, permission_required


class ClientsManager(Manager):
    """
    Manage the access to ``Client`` table.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Client)

    @permission_required(roles=[roles.SALES])
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
    def get(self, *args, **kwargs) -> typing.List[Client]:
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Client]:
        return super().all()

    @permission_required(roles=[roles.SALES])
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(*args, **kwargs):
        return super().delete(**kwargs)

    def filter_by_name(self, name_contains: str):
        return self.get(Client.full_name.contains(name_contains))


if __name__ == "__main__":
    from database.manager import engine

    session = Session(engine)

    manager = ClientsManager(session)

    client = manager.create(
        full_name="Thomas Menanteau",
        email="thomas.menanteau@example.co",
        phone="0611181228",
        enterprise="Airbus Helicopters",
        sales_contact_id=1,
    )

    if not client:
        exit()

    print(client.id, client.full_name)
