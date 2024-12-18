import importlib
import os.path
import psycopg
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import DBConnectionException
from configparser import ConfigParser
from sshtunnel import SSHTunnelForwarder


class Database:
    __db_config: dict[str, str]

    @staticmethod
    def __load_psql_config(filename='dbconnection.ini', section='postgresql') -> dict[str, str]:
        if filename == 'dbconnection.ini':
            filename = os.path.abspath(__file__).removesuffix('Database.py') + filename

        parser = ConfigParser()
        parser.read(filename)

        db_config = {}
        if parser.has_section(section):
            parser.has_section(section)
            params = parser.items(section)
            for param in params:
                db_config[param[0]] = param[1]
        else:
            raise DBConnectionException('Section {0} not found in the {1} file'.format(section, filename))
        return db_config

    @staticmethod
    def __load_ssh_config(filename='dbconnection.ini', section='ssh_tunnel') -> dict[str, str]:
        if filename == 'dbconnection.ini':
            filename = os.path.abspath(__file__).removesuffix('Database.py') + filename

        parser = ConfigParser()
        parser.read(filename)

        db_config = {}
        if parser.has_section(section):
            parser.has_section(section)
            params = parser.items(section)
            for param in params:
                db_config[param[0]] = param[1]
        else:
            raise DBConnectionException('Section {0} not found in the {1} file'.format(section, filename))
        return db_config

    @classmethod
    def connect(cls) -> bool:
        """
        Connects to the Database via SSH with the parameter given in dbconnection.ini
        :return: true if the connection to use for sql commands towards the database was established correctly
        """
        ssh_config = cls.__load_ssh_config()
        cls.__db_config = cls.__load_psql_config()

        ssh_tunnel = SSHTunnelForwarder(
            (ssh_config['database_host'], int(ssh_config['database_port'])),
                ssh_username=ssh_config['pie_username'],
                ssh_password=ssh_config['pie_password'],
                remote_bind_address=(ssh_config['bind_address'], int(ssh_config['bind_port'])),
                local_bind_address=(ssh_config['bind_address'], int(ssh_config['bind_port'])))

        ssh_tunnel.start()
        cls.__db_config['host'] = ssh_tunnel.local_bind_host
        cls.__db_config['port'] = ssh_tunnel.local_bind_port
        return ssh_tunnel.is_active

    @classmethod
    def disconnect(cls, ssh_tunnel):
        """
        Disconnects the given ssh_tunnel.
        """
        ssh_tunnel.close()

    @classmethod
    def run_sql_query(cls, query: str, response = True) -> [str]:
        """
        runs the given sql query with psycopg and returns the response from the db
        :return: list with the response of the database
        """
        try:
            with psycopg.connect(**cls.__db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    if response:
                        db_response = []
                        for record in cur:
                            db_response.extend(record)
                        return db_response
        except (psycopg.DatabaseError, Exception) as error:
            raise DBConnectionException(error)

    @classmethod
    def get_object(cls, oid: str) -> ClassBase | None:
        """
        Tries to find the object for the given oid in the database, and returns it, if not found "None" is returned
        Only works with objects from the type "ClassBase"
        :return: the found object or "None" if no object could be found
        """
        oid_key = oid [: 3]
        for classType in ClassType:
            if classType.value[1].__eq__(oid_key):
                found_class = getattr(importlib.import_module(f"pie_hardware.{classType.value[0]}"), classType.value[0], None)
                Database.connect()
                data = Database.run_sql_query("SELECT * FROM " + classType.name + " WHERE oid = '" + oid + "'")
                if not data:
                    return None
                return found_class.db_build_class(found_class, data)

    @classmethod
    def add_object(cls, persistent_object: ClassBase):
        print("Implementation missing")
        #TODO Implement

    @classmethod
    def update_object(cls, persistent_object: ClassBase):
        print("Implementation missing")
        #TODO Implement