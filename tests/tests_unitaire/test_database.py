import pytest
from epic_events.models.models import Department, Employee


class TestDatabase:
    def test_database_connection(self, connection):
        # test connect to database
        try:
            assert connection is not None
        except Exception as e:
            pytest.fail(f"Échec de la connexion à la base de données : {e}")

    def test_gestion_in_db(self, connection, dummy_employee_gestion):
        assert dummy_employee_gestion in connection.query(Employee).all()
        assert dummy_employee_gestion.department.name == "Gestion"

    def test_commercial_in_db(self, connection, dummy_employee_commercial):
        assert dummy_employee_commercial in connection.query(Employee).all()
        assert dummy_employee_commercial.department.name == "Commercial"

    def test_support_in_db(self, connection, dummy_employee_support):
        assert dummy_employee_support in connection.query(Employee).all()
        assert dummy_employee_support.department.name == "Support"
