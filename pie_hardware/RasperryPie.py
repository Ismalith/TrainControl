import inspect
import random
import re
from typing import override
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadInitializationException, RasperryException, BadAddressException
from database.Database import Database


class RasperryPie(ClassBase):
    """
    Rasperry Pie

    The computer to control the different parts of the tracks as well as be the database and the master planner
    """
    __master = False
    __database = False



    """
    START create functions
    """
    def __init__(self, name:str, master:bool = False, database:bool = False, oid:str = None):
        """
        Initialize the Rasperry Pie, do not use manually
        """
        caller_stack= inspect.stack()
        legal_db_call = False
        if oid is not None:
            for line in caller_stack:
                if "Database.py" in str(line):
                    legal_db_call = True
            if not legal_db_call:
                raise BadInitializationException("There was an attempt to set an oid manually, this is ONLY allowed for the database to load already constructed classes")
            super().__init__(ClassType.RASPERRYPIE, name, oid)
        else:
            super().__init__(ClassType.RASPERRYPIE, name)

        self.__master = master
        self.__database = database
        if not legal_db_call:
            self.__db_write_to_db__()
    """
    END create functions
    """



    """
    START db functions
    """
    @classmethod
    def __db_build_class__(cls, data:list):
        """
        puts the given parameter in this Rasperry_Pie object, only to be used by the database to load an already existing Rasperry_Pie
        from the database, to create a new Rasperry_Pie, use the constructor directly and NEVER set the parameter "oid"
        :return: the Rasperry_Pie object with the given parameter
        """
        new_rasperry_pie = object.__new__(cls)
        new_rasperry_pie.__init__(data[1], data[2], data[3], data[0])
        return new_rasperry_pie


    @override
    def __db_write_to_db__(self):
        sql_insert = "INSERT INTO rasperrypie (oid, name, master, database) VALUES ('" + self.get_oid() + "','" + self.get_name() + "','" + str(self.is_master()) + "','" + str(self.is_database()) + "')"
        Database.run_sql_query(sql_insert, False)


    def __delete_my_gpio_connections__(self):
        sql_statement = ""
        for class_type in ClassType:
            if str(class_type.value).__contains__("['gpio', 'integer']"):
                sql_statement = sql_statement + "UPDATE " + class_type.name + " SET rasperrypie = NULL, gpio = NULL WHERE rasperrypie = '" + self.get_oid() + "';"

        Database.run_sql_query(sql_statement, False)


    def __delete_my_i2c_connections__(self):
        sql_statement = ""
        for class_type in ClassType:
            if str(class_type.value).__contains__("['i2caddress', 'string']"):
                sql_statement = sql_statement + "UPDATE " + class_type.name + " SET rasperrypie = NULL, i2caddress = NULL WHERE rasperrypie = '" + self.get_oid() + "';"

        Database.run_sql_query(sql_statement, False)
    """
    END db functions
    """



    """
    START public general functions
    """
    @classmethod
    def create_new(cls, name:str, master:bool = False, database:bool = False):
        """
        Creates a new rasperry pie object and writes it into the database, also creates the reservations list for it's gpios
        :param name: the name for the new rasperry pie
        :param master: set true if this rasperry pie shall be the new master of the system, there can only be one
        :param database: set true if this rasperry pie shall be the new database of the system, there can only be one
        """
        if name is None:
            highest_generic_name = Database.run_sql_query("SELECT name FROM rasperrypie WHERE name ~ '^RasperryPie \\d+$' ORDER BY name DESC LIMIT 1")
            name = "RasperryPie " + str(int(str(highest_generic_name).rsplit(" ")[1]) + 1)
        else:
            found_rasperry_pies = Database.run_sql_query("SELECT count(oid) FROM rasperrypie WHERE name = '" + name + "'")
            if found_rasperry_pies > 0:
                raise BadInitializationException("A rasperry pie with the name " + name + " is already in the database")

        if master:
            found_master = Database.run_sql_query("SELECT name FROM rasperrypie WHERE master = true")
            if isinstance(found_master, str):
                raise BadInitializationException("There is already the rasperry pie " + found_master + " defined as a master, there can only be one master rasperry pie in the system")
            elif found_master is not None:
                raise BadInitializationException("There are already two or more rasperry pie defined as master, this should be impossible, something went terribly wrong")

        if database:
            found_database = Database.run_sql_query("SELECT name FROM rasperrypie WHERE database = true")
            if isinstance(found_database, str):
                raise BadInitializationException("There is already the rasperry pie " + found_database + " defined as a database, there can only be one database rasperry pie in the system")
            elif found_database is not None:
                raise BadInitializationException("There are already two or more rasperry pie defined as database, this should be impossible, something went terribly wrong")


        new_rasperry_pie = object.__new__(cls)
        new_rasperry_pie.__init__(name, master, database)
        return new_rasperry_pie


    @override
    def save(self):
        """
        Saves the current state of this rasperry pie into the database
        """
        print("Noch nicht implementiert RasperryPie.save")


    @override
    def shutdown(self):
        """
        Makes the raspberry pie ready for shut down
        """
        self.save()
    """
    END public general functions
    """



    """
    START public specific functions
    """
    @classmethod
    def get_for_id(cls, name: str = None):
        """
        Returns the rasperry pie that has the given name, if the whole system only runs on one rasperry pie, the name is not necessary
        :param name: the name of the rasperry pie that is requested
        :return: the rasperry pie that has the given id
        """
        if name is None:
            found_rasperry = Database.run_sql_query("SELECT oid FROM rasperrypie")
        else:
            found_rasperry = Database.run_sql_query("SELECT oid FROM rasperrypie WHERE name = '" + name + "'")

        if found_rasperry is None:
            raise RasperryException("No rasperry was found for the given name: " + str(name))

        if not isinstance(found_rasperry, str):
            if name is None:
                raise RasperryException(
                    "There was an attempt to call for a rasperry pie without a given name, while the database contained more than one rasperry, this only is possible if only one rasperry is registered")
            raise RasperryException("There was more than one rasperry found for the given name " + str(name))

        return RasperryPie(Database.get_object_for_oid(found_rasperry))


    def is_master(self) -> bool:
        """
        Returns if this rasperry pie is the master of the system
        :return: true if this rasperry pie is the system master
        """
        return self.__master


    def is_database(self) -> bool:
        """
        Returns if this rasperry pie is the database of the system
        :return: true if this rasperry pie is the system database
        """
        return self.__database


    def gpio_pin_is_free(self, gpio_pin: int):
        """
        Checks if the pin with the given integer address is free or already in use
        :return: true if the pin is not in use
        """
        if 0 > gpio_pin > 27:
            raise BadAddressException("Attempt to ask if a gpio pin outside the possible range  from 0 to 27 is free\n"
                                "requested gpio pin address: " + str(gpio_pin))

        if gpio_pin == 2 or gpio_pin == 3:
            raise BadAddressException("Attemt to ask if a gpio pin " + str(gpio_pin) + " on a rasperry pie is free,"
                                      " those pins are always reserved for the i2c connections")

        sql_statement = ""
        number_of_fitting_types = 0
        for class_type in ClassType:
            if str(class_type.value).__contains__("['gpio', 'integer']"):
                if number_of_fitting_types == 0:
                    sql_statement = "SELECT name FROM " + sql_statement + class_type.name + " WHERE rasperrypie = '" + self.get_oid() + "' AND gpio = " + str(gpio_pin)
                else:
                    sql_statement = sql_statement + " UNION SELECT name FROM " + class_type.name + " WHERE rasperrypie = '" + self.get_oid() + "' AND gpio = " + str(gpio_pin)

                number_of_fitting_types = number_of_fitting_types + 1

        found_user = Database.run_sql_query(sql_statement)

        if isinstance(found_user, str):
            raise BadAddressException("The pin " + str(gpio_pin) + " on rasperry pie " + self.get_name() + " is already taken by " + found_user)
        elif isinstance(found_user, list):
            found_user_string = ""
            for user_name in found_user:
                found_user_string = found_user_string + ", " + user_name

            raise BadAddressException("The gpio pin " + str(gpio_pin) + " on rasperry pie " + self.get_name() + " is already taken by multiple users, "
                                      "this should not be possible and hints to a deeper problem or manual alteration of the database\n"
                                      "Found user: " + found_user_string)
        return True


    def i2c_is_free(self, address:str):
        if not re.fullmatch(r'^0x[0-7][0-9a-fA-F]$', address):
            raise BadAddressException("Asked if an address on rasperry pie " + self.get_name() + " was available with a non hex address " + address)
        elif re.fullmatch(r'^0x0[0-7]$', address):
            raise BadAddressException("Attempt to initialize Ina219PowerSensor " + self.get_name() + " converter with a value below 0X08, only values of 0x08 or above are allowed " + address)
        elif re.fullmatch(r'^0x7[8-9a-fA-F]$', address):
            raise BadAddressException("Attempt to initialize Ina219PowerSensor " + self.get_name() + " converter with a value above 0X77, only values of 0x77 or below are allowed " + address)

        sql_statement = ""
        number_of_fitting_types = 0
        for class_type in ClassType:
            if str(class_type.value).__contains__("['i2caddress', 'string']"):
                if number_of_fitting_types == 0:
                    sql_statement = ("SELECT name FROM " + sql_statement + class_type.name + " WHERE rasperrypie = '" +
                                     self.get_oid() + "' AND i2caddress = '" + str(address) + "'")
                else:
                    sql_statement = (sql_statement + " UNION SELECT name FROM " + class_type.name +
                                     " WHERE rasperrypie = '" + self.get_oid() + "' AND i2caddress = '" + str(address) + "'")

                number_of_fitting_types = number_of_fitting_types + 1

        found_user = Database.run_sql_query(sql_statement)
        if isinstance(found_user, str):
            raise BadAddressException("The i2c address " + str(address) + " on rasperry pie " + self.get_name() + " is already taken by " + found_user)
        elif isinstance(found_user, list):
            found_user_string = ""
            for user_name in found_user:
                found_user_string = found_user_string + ", " + user_name

            raise BadAddressException("The i2c address " + str(address) + " on rasperry pie " + self.get_name() + " is already taken by multiple users, "
                                      "this should not be possible and hints to a deeper problem or manual alteration of the database\n"
                                      "Found user: " + found_user_string)
        return True
    """
    END public specific functions
    """