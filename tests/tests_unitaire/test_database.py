import pytest


class TestDatabase:
    def test_database_connection(self, connection):
        # test connect to database
        try:
            assert connection is not None
        except Exception as e:
            pytest.fail(f"Échec de la connexion à la base de données : {e}")
