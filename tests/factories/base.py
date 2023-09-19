import factory
from epic_events.data import conf


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = conf.Session
        sqlalchemy_session_persistence = "commit"
