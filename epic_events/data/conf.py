import os
import sentry_sdk
import logging
from sentry_sdk.scrubber import EventScrubber
from sentry_sdk.integrations.logging import LoggingIntegration
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

sentry_sdk.init(
    dsn=os.getenv("DNS"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    integrations=[
        LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        ),
    ],
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    # prevent sending sensitivedata to logging
    send_default_pii=False,
    event_scrubber=EventScrubber(),  # this is set by default
)


def start_db():
    Base.metadata.create_all(engine)
