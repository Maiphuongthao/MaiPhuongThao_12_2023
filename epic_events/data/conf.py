import logging
import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.scrubber import EventScrubber
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

file = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

path = ".ssh/secret.txt"
pub_path = ".ssh/secret.txt.pub"
with open(os.path.join(file, path)) as f:
    key = f.read()

with open(os.path.join(file, pub_path)) as f:
    pub_key = f.read()

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
