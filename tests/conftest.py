import pytest
import os
from sqlalchemy import create_engine, event, URL, text
from epic_events.models import models
from epic_events.data import conf
from dotenv import load_dotenv

load_dotenv()

database_name = "testdb"
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_type = os.getenv("DB_TYPE")


# define fixture that will setup and teardown the database, define database connection
@pytest.fixture(scope="session")
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
    connection = engine.connect()

    def teardown():
        query = text(f"DROP DATABASE {database_name};")
        connection.execute(query)
        connection.close()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture(scope="session", autouse=True)
def setup_db(connection, request):
    """here to setup test db
    creates all db tables as declared in SQLAlchemy models then drop them after finishing the test
    fixture runs automatically due to autouse
    """
    # models.Base.metadata.bind = connection
    print(f"connection:{connection}")
    models.Base.metadata.create_all(bind=connection)

    def teardown():
        models.Base.metadata.drop_all(bind=connection)

    request.addfinalizer(teardown)


# transaction test
# @pytest.fixture(autouse=True)
# def session(connection, request):
#     session = conf.Session(bind=connection)
#     session.begin_nested()

#     @event.listens_for(session, "after_transaction_end")
#     def restart_savepoint(db_session, transaction):
#         if transaction.nested and not transaction._parent.nested:
#             session.expire_all()
#             session.begin_nested()

#     def teardown():
#         conf.Session.remove()
#         session.rollback()

#     request.addfinalizer(teardown)
#     return session
