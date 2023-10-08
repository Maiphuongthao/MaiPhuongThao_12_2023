import os

import click

from epic_events.controller import cli
from epic_events.data import conf
from epic_events.data.dao import DepartmentDao

path_file = os.path.dirname(__file__)
test_sql_path = "tests/test_data.sql"
data_path = os.path.join(path_file, test_sql_path)


depart_dao = DepartmentDao()
if __name__ == "__main__":
    conf.start_db()

    if not depart_dao.get_all():
        click.echo("Data is empty, create new test.")
        cli.execute_test_sql(data_path)
    # launch program
    cli.cli()
