from epic_events.view import view
from epic_events.data.dao import EmployeeDao, DepartmentDao
from argon2 import PasswordHasher, exceptions
from cryptography.hazmat.primitives import serialization
import jwt
import click
from typing import Union, Tuple
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
import os, textwrap, stat
from dotenv import load_dotenv

load_dotenv()

netrc_host = os.getenv("HOST")
class LoginController:
    def __init__(self):
        self.login_view = view.LoginView()

    def authentification(self, relogin):
        """
        verify email and password then create a token with RS256 - asymmetric algorithm
        """
        credential = self.read_credentials(netrc_host) is not None
        if relogin: credential = False
        if not credential:
            (email, password) = self.login_view.login_get_username_and_password()
            try:
                employee = EmployeeDao.get_by_email(email)
            except IndexError:
                print("\nVotre addresse email n'est pas correct.")
                exit()
            try:
                h = PasswordHasher()
                h.verify(employee.password, password)
                secret_key = os.getenv("SECRET_KEY")
                private_key = serialization.load_pem_private_key(secret_key.encode(), password=b'')
            
                payload = {
                    "email":email,
                    "departement_id": employee.department_id,
                    "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=500)
                }
                token = jwt.encode(payload=payload, key=private_key, algorithm='RS256')
                self.write_netrc(netrc_host, employee, token)
                self.login_view.successful_login()
            except exceptions.VerifyMismatchError:
                print("Votre mot de passe n'est pas correct.")
        else:
            click.echo("Vous êtes déja connectés! 🔑")
            

    def write_netrc(host: str, user: str, token: str):
        """
        Store token with netrc file, create and modify an entry
        """
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
            login {user}
            password {token}
            """
                ).format(host=normalized_host, user=user, token=token)
            )
        os.chmod(os.path.expanduser("~/.netrc"), stat.S_IRUSR | stat.S_IWUSR)
        return True
    

    def find_netrc_token(self, machine: str, raise_errors=False):
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
                _netrc = netrc(netrc_path).authenticators(host)
                if _netrc:
                    login_i = 0 if _netrc[0] else 1
                    return (_netrc[login_i], _netrc[2])
            except (NetrcParseError, IOError):
                if raise_errors:
                    raise

        except (ImportError, AttributeError):
            pass


    def read_credentials(self, machine: str) -> Union[Tuple[str, str], None]:
        """
        Reads user credentials if there's an existing token
        """
        user, token = None, None
        auth = self.find_netrc_token(machine, True)
        if auth and auth[0] and auth[1]:
            user = auth[0]
            token = auth[1]
            return (user, token)
        



        
        
    