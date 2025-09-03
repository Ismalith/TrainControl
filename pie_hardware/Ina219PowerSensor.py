import inspect
from typing import override
from ina219 import INA219
from ina219 import DeviceRangeError
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadAddressException, Ina219AmpSensException, BadInitializationException
import re
from database.Database import Database
from pie_hardware.RasperryPie import RasperryPie


class Ina219PowerSensor(ClassBase):
    """
    INA219 Power Sensor

    The sensor to measure if a locomotive is on a part of the track and the current demanded power
    """
    __rp_pie: RasperryPie
    __MAX_EXPECTED_AMPS = 2.0
    __SHUNT_OHMS = 0.1
    __address: str = None



    """
    START create functions
    """
    def __init__(self, name:str, rp_pie:RasperryPie, address:str = None, oid:str = None):
        """
        Initialize the INA 219 Power Sensor, do not use manually
        """
        if not re.fullmatch(r'^0x[0-7][0-9a-fA-F]$', address):
            raise BadAddressException("Attempt to initialize an Ina219PowerSensor converter with a non hex address")

        caller_stack = inspect.stack()
        legal_db_call = False
        if oid is not None:
            for line in caller_stack:
                if "Database.py" in str(line):
                    legal_db_call = True
            if not legal_db_call:
                raise BadInitializationException("There was an attempt to set an oid manually, this is ONLY allowed for the database to load already constructed classes")
            super().__init__(ClassType.INA219POWERSENSOR, name, oid)
        else:
            super().__init__(ClassType.INA219POWERSENSOR, name)

        self.__address = address
        self.__rp_pie = rp_pie
        if not legal_db_call:
            self.__db_write_to_db__()
    """
    END create functions
    """



    """
    START db functions
    """
    @classmethod
    def __db_build_class__(cls, data):
        """
        Puts the given parameter in this relay object, only to be used by the database to load an already existing relay
        from the database, to create a new relay, use the constructor directly and NEVER set the parameter "oid"
        :return: the Relay object with the given parameter
        """
        new_ina219_sensor = object.__new__(cls)
        new_ina219_sensor.__init__(data[2], data[1], data[3], data[0])
        return new_ina219_sensor


    @override
    def __db_write_to_db__(self):
        if self.__address is not None:
            sql_insert = "INSERT INTO ina219powersensor (oid, name, rasperrypie, i2caddress) VALUES ('" + self.get_oid() + "', '" + self.get_name() + "', '" + str(self.get_rasperry_pie().get_oid()) + "', '" + self.get_address() + "')"
            Database.run_sql_query(sql_insert, False)
        else:
            sql_insert = "INSERT INTO ina219powersensor (oid, name, rasperrypie) VALUES ('" + self.get_oid() + "', '" + self.get_name() + "', '" + str(self.get_rasperry_pie().get_oid()) + "')"
            Database.run_sql_query(sql_insert, False)
    """
    END db functions
    """



    """
    START public general functions
    """
    @classmethod
    def create_new(cls, rasperry_pie: RasperryPie, address:str = None, name: str = None):
        """
        Creation methode to create and write a new ina219powersensor to the database, only create new ina219powersensor with this method
        :param rasperry_pie: the rasperry pie that is controlling this power sensor
        :param address: the i2c address from the rasperry pie that will be controlling this power sensor,
        :param name: the name for the power sensor, if not chosen manually the new power sensor will get the name "PowerSensor x" where x is the new highest numer of all existing "PowerSensor x"
        :return: the newly created power sensor
        """

        if name is None:
            highest_generic_name = Database.run_sql_query("SELECT name FROM ina219powersensor WHERE name ~ '^PowerSensor \\d+$' ORDER BY name DESC LIMIT 1")
            if highest_generic_name is not None:
                name = "PowerSensor " + str(int(str(highest_generic_name).rsplit(" ")[1]) + 1)
            else:
                name = "PowerSensor 1"
        else:
            found_power_sensors_with_same_name = int(Database.run_sql_query("SELECT count(oid) FROM ina219powersensor "
                "WHERE name = '" + name + "' AND rasperrypie = '" + rasperry_pie.get_oid() + "'"))
            if found_power_sensors_with_same_name > 0:
                raise BadInitializationException("A ina 219 power sensor with the name " + name + " is already in use on the same rasperry pie " + rasperry_pie.get_name())

        if address is not None:
            rasperry_pie.i2c_is_free(address)

        new_ina219_sensor = object.__new__(cls)
        new_ina219_sensor.__init__(name, rasperry_pie, address)
        return new_ina219_sensor


    @override
    def save(self):
        """
        Saves the current state of this rasperry pie into the database
        """
        print("Noch nicht implementiert Ina219PowerSensor.save")


    @override
    def shutdown(self):
        self.__db_write_to_db__()
    """
    END public general functions
    """



    """
    START public specific functions
    """
    def connect_to_i2c(self, rasperry_pie: RasperryPie, address: str):
        rasperry_pie.i2c_is_free(address)
        Database.run_sql_query("UPDATE ina219powersensor ips SET i2caddress = " + str(address) + " AND rasperrypie = '" +
                               rasperry_pie.get_oid() + "' WHERE ips.oid = '" + self.get_oid() + "'",False)

        self.__rp_pie = rasperry_pie
        self.__address = address


    def get_rasperry_pie(self):
        """
         Returns the rasperry pie that controls this power sensor
         :return: the rasperry pie, that controls this power sensor
         """
        return self.__rp_pie


    def get_address(self):
        """
        The hex address that the rasperry pie uses to control this power sensor
        :return: the address to control this power sensor
        """
        return self.__address


    def read_current(self):
        """
        Reads the current on the chip in amps
        :return: the current in amps
        """
        ina219 = INA219(self.__SHUNT_OHMS, self.__MAX_EXPECTED_AMPS, address=int(self.__address, 16))
        ina219.configure(ina219.RANGE_32V, ina219.GAIN_8_320MV)
        try:
            return "%.1f" % (ina219.current() / 1000)
        except DeviceRangeError:
            raise Ina219AmpSensException("Current overflow at Ina219AmpSensor " + self.__address)


    def read_power(self):
        """
        Reads the power on the chip in full watts
        :return: the power in watts
        """
        ina219 = INA219(self.__SHUNT_OHMS, self.__MAX_EXPECTED_AMPS, address=int(self.__address, 16))
        ina219.configure(ina219.RANGE_32V, ina219.GAIN_8_320MV)
        try:
            return "%.1f" % (ina219.power() / 1000)
        except DeviceRangeError:
            raise Ina219AmpSensException("Current overflow at Ina219AmpSensor " + self.__address)
    """
    END public specific functions
    """