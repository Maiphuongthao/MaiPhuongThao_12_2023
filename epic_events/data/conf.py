import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()

db_type = os.getenv("DB_TYPE")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")

url = URL.create(
    drivername=db_type,
    username=db_user,
    password=db_password,
    host=db_host,
    database=db_name,
)

# SQLAlchemy session
engine = create_engine(url)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

Base = declarative_base()


def start_db():
    Base.metadata.create_all(engine)
