import importlib
import os.path
import psycopg
import importlib.util
import os
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import DBConnectionException, DBException
from configparser import ConfigParser
from sshtunnel import SSHTunnelForwarder
from core.Tools import Tools


class Database:
    __db_config: dict[str, str]

    @staticmethod
    def __load_psql_config(path = "/database",filename='dbconnection.ini', section='postgresql') -> dict[str, str]:
        return Tools.ini_reader(path, filename, section)


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
    def disconnect(cls, ssh_tunnel):
        """
        Disconnects the given ssh_tunnel.
        :param ssh_tunnel: the ss tunnel object that is to be closed
        """
        ssh_tunnel.close()


    @classmethod
    def run_sql_query(cls, query: str, response = True) -> list[str] | str | None:
        """
        runs the given sql query with psycopg and returns the response from the db
        :param query: the sql command to run as a string
        :param response: if true, the return value of the query is returned by this function,
            if set true while the sql query doesn't return a value, this will result in an error
        :return: list with the response of the database
        """
        #First build the connection, if it isn't already established, _Database__db_config only exists if the connection is established
        if not hasattr(cls, '_Database__db_config'):
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

        #Now execute the sql query
        try:
            with psycopg.connect(**cls.__db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    if response:
                        db_response = []
                        for record in cur:
                            db_response.extend(record)
                        if db_response.__len__() == 1:
                            return db_response[0]
                        elif db_response.__len__() == 0:
                            return None
                        else:
                            return db_response
        except (psycopg.DatabaseError, Exception) as error:
            raise DBConnectionException(error)


    @classmethod
    def get_object_for_oid(cls, oid: str):
        """
        Tries to find the object for the given oid in the database, and returns it, if not found "None" is returned
        Only works with objects from the type "ClassBase"
        :param oid: the oid that identifies the searched object
        :return: the found object or "None" if no object could be found
        """
        oid_key = oid [: 3]
        root_dir = str(os.path.dirname(os.path.abspath(__file__)).removesuffix("\\database"))

        for classType in ClassType:
            if classType.value[1].__eq__(oid_key):
                packages = next(os.walk(root_dir))[1]
                if ".git" in packages:
                    packages.remove(".git")
                if ".idea" in packages:
                    packages.remove(".idea")
                if "__pycache__" in packages:
                    packages.remove("__pycache__")

                package_name = None
                for package in packages:
                    for filenames, dirpath, dirnames in os.walk(root_dir + "\\" + package):
                        if classType.value[0] in str(dirnames) and "__pycache__" not in filenames:
                            package_name = filenames.rsplit("\\")
                            package_name = package_name[len(package_name) - 1]
                found_class = getattr(importlib.import_module(f"{package_name}.{classType.value[0]}"), classType.value[0], None)
                data = Database.run_sql_query("SELECT * FROM " + classType.name + " WHERE oid = '" + oid + "'")
                if not data:
                    return None
                return found_class.__db_build_class__(data)
        raise DBException("String " + oid_key + " could not be matched to any class")

    @classmethod
    def get_object_for_name(cls, name:str, class_type: ClassType):
        """
        Tries to find the object for the given combination from id and class type, returns the amount found, if
        there was more than one object that fit the given parameter, the amount of objects found is returned.
        :param name: the name of the requested object
        :param class_type: the class type of the requested object
        """
        number_objects_found = cls.run_sql_query("SELECT COUNT(oid) FROM " + class_type.value[0] + " WHERE name = '" + name + "'")
        if number_objects_found  != 1:
            return number_objects_found

        found_object_oid = Database.run_sql_query("SELECT oid FROM " + class_type.value[0] + " WHERE name = '" + name + "'")
        if isinstance(found_object_oid, str):
            return Database.get_object_for_oid(found_object_oid)

        return None


    @classmethod
    def add_object(cls, persistent_object: ClassBase):
        print(persistent_object.get_name())
        print("Implementation missing add_object in Database.py")
        #TODO Implement


    @classmethod
    def update_object(cls, persistent_object: ClassBase):
        print("Implementation missing update_object in Database.py")
        #TODO Implement