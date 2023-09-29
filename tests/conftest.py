import pytest
import os
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker, scoped_session
from epic_events.models import models
from dotenv import load_dotenv
from argon2 import PasswordHasher


load_dotenv()

database_name = "testdb"
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_type = os.getenv("DB_TYPE")

path_file = os.path.dirname(__file__)
test_sql_path = "permission.sql"
data_path = os.path.join(path_file, test_sql_path)


# define fixture that will setup and teardown the database, define database connection
@pytest.fixture(scope="session", autouse=True)
def connection(request):
    url = URL.create(
        drivername=db_type,
        username=db_user,
        password=db_password,
        host=db_host,
        database=db_name,
    )
    engine = create_engine(url)
    with engine.connect() as connection:
        query = text(f"CREATE DATABASE {database_name};")
        connection.execute(query)

    # Create a new engine/connection that will actually connect
    # to the test database we just created. This will be the
    # connection used by the test suite run.

    test_url = URL.create(
        drivername=db_type,
        username=db_user,
        password=db_password,
        host=db_host,
        database=database_name,
    )
    engine = create_engine(test_url)

    Session = scoped_session(sessionmaker(bind=engine))
    connection = Session()

    models.Base.metadata.create_all(engine)
    yield connection

    def teardown():
        query = text(f"DROP DATABASE {database_name};")
        connection.execute(query)
        connection.close()

    request.addfinalizer(teardown)


@pytest.fixture(scope="session", autouse=True)
def dummy_department_gestion(connection):
    department = models.Department(name="Gestion")
    connection.add(department)
    connection.commit()
    return department


@pytest.fixture(scope="session", autouse=True)
def dummy_department_gestion(connection):
    department = models.Department(id=1, name="Gestion")
    connection.add(department)
    connection.commit()
    return department


@pytest.fixture(scope="session", autouse=True)
def dummy_department_commercial(connection):
    department = models.Department(id=2, name="Commercial")
    connection.add(department)
    connection.commit()
    return department


@pytest.fixture(scope="session", autouse=True)
def dummy_department_support(connection):
    department = models.Department(id=3, name="Support")
    connection.add(department)
    connection.commit()
    return department


@pytest.fixture(scope="session", autouse=True)
def dummy_permissions(connection):
    f = open(data_path, "r")
    sql_file = f.read()
    f.close()
    commands = sql_file.split(";")
    for command in commands:
        try:
            if command.strip() != "":
                connection.execute(command)
        except IOError as msg:
            print(f"Command skipped: {msg}")
    connection.commit()


@pytest.fixture(scope="session", autouse=True)
def dummy_employee_gestion(connection):
    h = PasswordHasher()
    pasword = h.hash("Password12@")
    employee = models.Employee(
        name="Gestion1", email="gestion1@test.com", password=pasword, department_id=1
    )
    connection.add(employee)
    connection.commit()
    return employee


@pytest.fixture(scope="session", autouse=True)
def dummy_employee_commercial(connection):
    h = PasswordHasher()
    pasword = h.hash("Password12@")
    employee = models.Employee(
        name="Commercial1",
        email="commercial1@test.com",
        password=pasword,
        department_id=2,
    )
    connection.add(employee)
    connection.commit()
    return employee


@pytest.fixture(scope="session", autouse=True)
def dummy_employee_support(connection):
    h = PasswordHasher()
    pasword = h.hash("Password12@")
    employee = models.Employee(
        name="Support1", email="support1@test.com", password=pasword, department_id=3
    )
    connection.add(employee)
    connection.commit()
    return employee
