import inspect
from typing import override
from core.ClassBase import ClassBase
from core.ClassType import ClassType
#import RPi.GPIO as GPIO TODO sobald auf einem Rasperry Pie, diese Zeilen wieder einfügen
from core.Exceptions import GPIOException, BadInitializationException
from database.Database import Database
from pie_hardware.RasperryPie import RasperryPie


class Relay(ClassBase):
    """
    Relay

    The normally open and normally closed relay
    """
    __rp_pie: RasperryPie
    __gpio:int
    __closed:bool



    """
    START create functions
    """
    def __init__(self, name:str, rp_pie: RasperryPie, gpio:int = None, closed: bool = False, oid: str = None):
        """
        Initialize the Relay, do not use manually
        """
        caller_stack = inspect.stack()
        legal_db_call = False
        if oid is not None:
            for line in caller_stack:
                if "Database.py" in str(line):
                    legal_db_call = True
            if not legal_db_call:
                raise BadInitializationException(
                    "There was an attempt to set an oid manually, this is ONLY allowed for the database to load already constructed classes")
            super().__init__(ClassType.RELAY, name, oid)
        else:
            super().__init__(ClassType.RELAY, name)

        self.__rp_pie = rp_pie
        self.__gpio = gpio
        #GPIO.setmode(GPIO.BCM) TODO sobald auf einem Rasperry Pie, diese Zeilen wieder einfügen
        #GPIO.setup(self.__gpio, GPIO.OUT)
        #if closed:
            #GPIO.output(self.__gpio, GPIO.LOW)
        #else:
            #GPIO.output(self.__gpio, GPIO.HIGH)
        self.__closed = closed
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
        new_relay = object.__new__(cls)
        new_relay.__init__(data[2], data[1], data[3], data[4], data[0])
        return new_relay


    @override
    def __db_write_to_db__(self):
        if self.__gpio is None:
            sql_insert = ("INSERT INTO relay (oid, name, rasperrypie, closed) VALUES ('" + self.get_oid() + "','" + self.get_name() + "','" +
                          str(self.get_rasperry_pie().get_oid()) + "','" + str(self.is_closed()) + "')", None)
        else:
            sql_insert = ("INSERT INTO relay (oid, name, rasperrypie, gpio, closed) VALUES ('" + self.get_oid() + "','" + self.get_name() + "','" +
                          str(self.get_rasperry_pie().get_oid()) + "'," + str(self.get_gpio()) + ",'" + str(self.is_closed()) + "')")
        Database.run_sql_query(sql_insert, False)
    """
    END db functions
    """



    """
    START public general functions
    """
    @classmethod
    def create_new(cls, gpio_pin: int = None, name:str = None, rasperry_pie: RasperryPie = None, closed: bool = False):
        """
        Creation methode to create and write a new relay to the database, only create new relay with this method
        :param gpio_pin: the gpio pin that will be controlling this relay,
        :param name: the name for the relay, if not chosen manually the new relay will get the name "Relay x" where x is the new highest numer of all existing "Relay x"
        :param rasperry_pie: the rasperry pie that is controlling this relay
        :param closed: set true to close the relay
        :return: the newly created relay
        """
        if name is None:
            highest_generic_name = Database.run_sql_query(
                "SELECT name FROM relay WHERE name ~ '^Relay \\d+$' ORDER BY name DESC LIMIT 1")
            if highest_generic_name is not None:
                name = "Relay " + str(int(str(highest_generic_name).rsplit(" ")[1]) + 1)
            else:
                name = "Relay 1"
        else:
            found_relays_with_same_name = Database.run_sql_query("SELECT count(oid) FROM relay WHERE name = '" + name + "' AND rasperrypie = '" + rasperry_pie.get_oid() + "'")
            if found_relays_with_same_name> 0:
                raise BadInitializationException("There was already a Relay with the name " + name + " for the rasperry pie " +rasperry_pie.get_name())

        if gpio_pin is not None:
            rasperry_pie.gpio_pin_is_free(gpio_pin)

        new_relay = object.__new__(cls)
        new_relay.__init__(name, rasperry_pie, gpio_pin, closed=closed)
        return new_relay


    @override
    def save(self):
        """
        Saves the current state of this relay into the database
        """
        print("Noch nicht implementiert Relay.save")


    def shutdown(self):
        """
        Cleans the gpio up, to avoid "already in use" warnings on reinitializing, only to be used at the end of a program
        :return: nothing
        """
        GPIO.cleanup()
        self.__db_write_to_db__()
    """
    END public general functions
    """



    """
    START public specific functions
    """
    def connect_to_gpio(self, rasperry_pie: RasperryPie, gpio_pin: int):
        """
        Check if the given pin address is valid, throws exception if not
        :param rasperry_pie: the rasperry pie that will be controlling this relay
        :param gpio_pin: The GPIO that will be controlling this relay
        :return: nothing
        """
        rasperry_pie.gpio_pin_is_free(gpio_pin)
        Database.run_sql_query("UPDATE relay SET gpio = " + str(gpio_pin) + " AND rasperrypie = '" + rasperry_pie.get_oid() + "' WHERE relay.oid = '" + self.get_oid() + "'", False)
        self.__rp_pie = rasperry_pie
        self.__gpio = gpio_pin

    def close(self):
        """
        Sets the relay closed by setting the GPIO to HIGH
        :return: nothing
        """
        GPIO.output(self.__gpio, GPIO.LOW)
        self.__closed = True


    def open(self):
        """
        Sets the relay open by setting the GPIO to LOW
        :return: nothing
        """
        GPIO.output(self.__gpio, GPIO.HIGH)
        self.__closed = False


    def get_rasperry_pie(self):
        """
        Returns the rasperry pie that controls this relay
        :return: the rasperry pie, that owns this relay
        """
        return self.__rp_pie



    def get_gpio(self):
        """
        The number of the gpio pin that controls this relay
        :return: the number of the gpio pin that controls this relay
        """
        return self.__gpio


    def is_closed(self):
        """
        Returns true in the relay is closed
        :return: true if the relay is closed
        """
        return self.__closed
    """
    END public specific functions
    """