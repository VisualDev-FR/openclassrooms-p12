import sqlalchemy
from sqlalchemy.orm import Session
from database.manager import engine
from models.employees import Employee, Department
from authentification.decorators import login_required


def create(full_name: str, email: str, password: str, department: Department):
    with Session(engine) as session:
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=department,
        )

        new_employee.set_password(password)

        session.add(new_employee)
        session.commit()


@login_required
def get(email: str, password: str):
    session = Session(engine)

    request = sqlalchemy.select(Employee).where(Employee.email == email)

    employee = session.scalar(request)

    print(employee.full_name)

    # for employee in session.scalars(request):

    #     valid_password = employee.check_password(password)

    #     print(employee.full_name, valid_password)


if __name__ == "__main__":
    create(
        full_name="Thomas, Menanteau",
        email="example@epicevents.co",
        password="password",
        department=Department.SALES
    )
