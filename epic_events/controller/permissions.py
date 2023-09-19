import os
import textwrap
import stat
import jwt
import click
from jwt.exceptions import ExpiredSignatureError
from typing import Union, Tuple
from urllib.parse import urlparse
from dotenv import load_dotenv
from epic_events.data.dao import DepartmentDao, EmployeeDao, PermissionDao
from cryptography.hazmat.primitives import serialization


load_dotenv()

public_key = os.getenv("PUBLIC_KEY")
netrc_host = os.getenv("HOST")
employee_dao = EmployeeDao()
permission_dao = PermissionDao()
department_dao = DepartmentDao()


def write_netrc(host: str, entity: str, key: str):
    normalized_host = urlparse(host).netloc.split(":")[0]
    if normalized_host != "localhost" and "." not in normalized_host:
        return None
    machine_line = "machine %s" % normalized_host
    path = os.path.expanduser("~/.netrc")
    orig_lines = None
    with open(path) as f:
        orig_lines = f.read().strip().split("\n")
    with open(path, "w") as f:
        if orig_lines:
            skip = 0
            for line in orig_lines:
                if line == "machine " or machine_line in line:
                    skip = 2
                elif skip:
                    skip -= 1
                else:
                    f.write("%s\n" % line)
        f.write(
            textwrap.dedent(
                """\
        machine {host}
          login {entity}
          password {key}
        """
            ).format(host=normalized_host, entity=entity, key=key)
        )
    os.chmod(os.path.expanduser("~/.netrc"), stat.S_IRUSR | stat.S_IWUSR)
    return True


def _find_netrc_token(machine: str, raise_errors=False):
    """
    Check if there's a token in the netrc file of user machine, to prevent the need for a user to login everytime
    """
    NETRC_FILES = (".netrc", "_netrc")
    netrc_file = os.environ.get("NETRC")
    if netrc_file is not None:
        netrc_locations = (netrc_file,)
    else:
        netrc_locations = ("~/{}".format(f) for f in NETRC_FILES)

    try:
        from netrc import netrc, NetrcParseError

        netrc_path = None

        for f in netrc_locations:
            try:
                loc = os.path.expanduser(f)
            except KeyError:
                return

            if os.path.exists(loc):
                netrc_path = loc
                break

        if netrc_path is None:
            return

        ri = urlparse(machine)

        host = ri.netloc.split(":")[0]

        try:
            # breakpoint()
            _netrc = netrc(netrc_path).authenticators(host)
            if _netrc:
                login_i = 0 if _netrc[0] else 1
                return (_netrc[login_i], _netrc[2])
        except (NetrcParseError, IOError):
            if raise_errors:
                raise

    except (ImportError, AttributeError):
        pass


def read_credentials(machine: str) -> Union[Tuple[str, str], None]:
    """
    Reads user credentials if there's an existing token
    """
    user, token = None, None
    auth = _find_netrc_token(machine, True)
    if auth and auth[0] and auth[1]:
        user = auth[0]
        token = auth[1]
        return (user, token)


def is_authenticated(func):
    """
    Decode a token with an asymetric algorithm and check expiration
    """

    def wrapper(*args, **kwargs):
        try:
            get_payload()
            if func is not None:
                func()
        except ExpiredSignatureError:
            click.echo("Connection expirée, connectez vous à nouveau.")

    return wrapper


def get_token():
    credential = read_credentials(netrc_host)
    return credential[1]


def get_payload():
    token = get_token()
    key = serialization.load_pem_public_key(public_key.encode())
    return jwt.decode(token, key, algorithms=["RS256"])


def get_department():
    payload = get_payload()
    department = department_dao.get_by_id(payload["departement_id"])
    return department


def get_user_id():
    payload = get_payload()
    employee = department_dao.get_by_id(payload["email"])
    return employee


def ob_for_main_menu(func):
    """
    check permissions and return its ob_name then put show in main menu
    """

    def wrapper(*args, **kwargs):
        department = get_department()
        department_permissions = department.permissions
        obs = list(
            dict.fromkeys(
                [
                    permission_dao.get_by_id(department_permission.id).ob_name
                    for department_permission in department_permissions
                ]
            )
        )
        func(*args, **kwargs, objects=obs)

    return wrapper


def ob_for_actions_menu(func):
    """
    Check the permissions of user then return crud actions to menu
    """

    def wrapper(*args, **kwargs):
        department = get_department()
        employee = get_user_id()
        permissions = department.permissions
        permissions_list = [
            permission_dao.get_by_id(permission.id) for permission in permissions
        ]
        actions = list(
            dict.fromkeys(
                [
                    permission.ob_action
                    for permission in permissions_list
                    if permission.ob_name == kwargs["ob_name"]
                ]
            )
        )
        func(*args, **kwargs, actions=actions)

    return wrapper
