import inspect
import random

from core.ClassType import ClassType
from core.Exceptions import BadInitializationException, BadObjectException


class ClassBase:
    """
    All persistent classes have to inherit from this class,
    it organizes the synchronization of classes and the database
    """
    __oid = "xxx"
    __classType: ClassType
    __name: str = None


    """
    START create functions
    """
    def __new__(cls, *args, **kwargs):
        legal_call = False
        for line in inspect.stack():
            if ".cast_to_rasperry_pie()" in str(line):
                legal_call = True
                break
            elif ".cast_to_gpio()" in str(line):
                legal_call = True
                break

        if not legal_call:
            raise BadInitializationException("There was an attempt to call the constructor for a ClassBase class directly, NEVER do this, use the \"create_new()\" method")


    def __init__(self, class_type: ClassType, name:str, oid: str = None):
        """
        Base initialization for all persistent classes, sets the oid and the type of the created class
        :param class_type: the class type to identify the new class
        :param oid: to set an already existing oid, ONLY to use when reloading the relais from the database
        """
        from database.Database import Database

        if oid is None:
            if self.__oid != "xxx":
                raise BadInitializationException("Attempt to initialize a class that was already initialized")

            self.__oid = class_type.value[1] + str(random.randint(1000000, (1000000 * 10 - 1)))
            while Database.get_object_for_oid(self.__oid) is not None :
                self.__oid = class_type.value[1] + str(random.randint(1000000, (1000000 * 10 - 1)))

        else:
            legal_call = False
            for line in inspect.stack():
                if "Database.py" in str(line) or ".cast_to_" in str(line):
                    legal_call = True
                    break
            if not legal_call:
                raise BadInitializationException("There was an attempt to set an oid manually, this is ONLY allowed for the database to load already constructed classes")
            self.__oid = oid

        self.__classType = class_type
        self.__name = name
    """
    END create functions
    """



    """
    START db functions
    """
    @classmethod
    def __db_build_class__(cls, data):
        pass


    def __db_write_to_db__(self):
        pass
    """
    END db functions
    """



    """
    START public general functions
    """
    def get_oid(self):
        """
        Returns the oid of this class
        :return: oid
        """
        if self.__oid is None:
            raise BadObjectException("A class that inherited from ClassBase did not have an oid")
        return self.__oid


    def get_type(self):
        """
        Returns the type of this class
        :return: enum class type
        """
        return self.__classType


    def get_name(self):
        """
        Returns the name of the object
        """
        if self.__name is None:
            raise BadObjectException("A class that inherited from ClassBase did not have a name, oid: " + self.get_oid())
        return  self.__name


    def save(self):
        pass


    def shutdown(self):
        """
        Shutdown procedure for a clean and save exit.
        """
        pass
    """
    END public general functions
    """



    """
    START public specific functions
    """
    def cast_to_gpio(self):
        """
        Casts a ClassBase object to a Gpio Object
        WARNING: This new object is not synchronised with its original ClassBase object or other versions of itself
        :return: a new Gpio object
        """
        #from pie_hardware.Gpio import Gpio

        #new_gpio:Gpio = object.__new__(Gpio)
        #new_gpio.__init__(self.__getattribute__("_Gpio__rasperry_pie"), self.__getattribute__("_Gpio__pin"), self.__getattribute__("_Gpio__user"), self.get_oid())
        #return new_gpio


    def cast_to_i2c(self):
        """
        Casts a ClassBase object to a I2cConnection Object
        WARNING: This new object is not synchronised with its original ClassBase object or other versions of itself
        :return: a new I2cConnection object
        """
        #from pie_hardware.I2cConnection import I2cConnection

        #new_i2c_connection:I2cConnection = object.__new__(I2cConnection)
        #new_i2c_connection.__init__(self.__getattribute__("_I2cConnection__rasperry_pie"), self.__getattribute__("_I2cConnection__pin"), self.__getattribute__("_I2cConnection__user"), self.get_oid())
        #return new_i2c_connection

    #TODO ALl die anderen cast to hinzu fügen.
    """
    END public specific functions
    """