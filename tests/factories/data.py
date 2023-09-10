from epic_events.models import models
from base import BaseFactory

class UserFactory(BaseFactory):
    class Meta:
        abstract = True
        model = models.Employee

class ClientFactory(BaseFactory):
    class Meta:
        abstract = True
        models = models.Client

class EventFactory(BaseFactory):
    class Meta:
        abstract = True
        models = models.Event

class ContractFactory(BaseFactory):
    class Meta:
        abstract = True
        models = models.Contract

class DepartmentFactory(BaseFactory):
    class Meta:
        abstract = True
        models = models.Department