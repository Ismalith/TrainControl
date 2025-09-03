import inspect
from typing import override
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadInitializationException
from database.Database import Database


class Matrix(ClassBase):
    """
    Matrix

    The matrix that contains every and all track objects
    """
    __xlength:int
    __ylength:int
    __zlength:int



    """
    START create functions
    """
    def __init__(self, name:str, xlength:int, ylength:int, zlength:int, oid:str = None):
        """
        Initialize the Matrix, do not use manually
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
            super().__init__(ClassType.MATRIX, name, oid)
        else:
            super().__init__(ClassType.MATRIX, name)

        self.__xlength = xlength
        self.__ylength = ylength
        self.__zlength = zlength
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
        Puts the given parameter in this Matrix object, only to be used by the database to load an already existing matrix
        from the database, to create a new matrix, use the constructor directly and NEVER set the parameter "oid"
        :return: the Matrix object with the given parameter
        """
        new_matrix = object.__new__(cls)
        new_matrix.__init__(data[1], data[2], data[3], data[4], data[0])
        return new_matrix


    @override
    def __db_write_to_db__(self):
        dimensions = self.get_dimensions()
        sql_insert = ("INSERT INTO matrix (oid, name, xlength, ylength, zlength) VALUES ('" + self.get_oid() + "', '" + self.get_name() + "', '" +
                      str(dimensions[0]) + "'," + str(dimensions[1]) + ",'" + str(dimensions[2]) + "')")
        Database.run_sql_query(sql_insert, False)
    """
    END db functions
    """



    """
    START public general functions
    """
    @classmethod
    def create_new(cls, name:str, xlength:int, ylength:int, zlength:int):
        """
        Creation methode to create and write a new matrix to the database, only create new matrix with this method
        :param name: the name for the matrix, if not chosen manually the new relay will get the name "Matrix"
        :param xlength: the length of the matrix in µm (1/10000)
        :param ylength: the width of the matrix in µm (1/10000)
        :param zlength: the height of the matrix in µm (1/10000)
        :return: the newly created matrix
        """
        if Database.run_sql_query("SELECT name FROM matrix") is not None:
            raise BadInitializationException("There was already a Matrix, there can only be one per project")

        if Database.run_sql_query("SELECT name FROM plane") is not None:
            raise BadInitializationException("There was already a Plane defined without a matrix, a matrix can only be created when there are no planes defined already")

        if name is None:
            name = "Matrix"

        if xlength < 1 or ylength < 1 or zlength < 1:
            raise BadInitializationException("There was an attempt to create a new Matrix object with one of it's dimensions smaller than 1:\n" +
                                             "X length = " + str(xlength) + "\n" +
                                             "Y length = " + str(ylength) + "\n" +
                                             "Z length = " + str(zlength) + "\n")

        new_matrix = object.__new__(cls)
        new_matrix.__init__(name, xlength, ylength, zlength)
        return new_matrix


    @override
    def save(self):
        """
        Saves the current state of this matrix into the database
        """
        print("Noch nicht implementiert Matrix.save")


    def shutdown(self):
        """
        Cleans the matrix object up
        :return: nothing
        """
        self.__db_write_to_db__()
    """
    END public general functions
    """



    """
    START public specific functions
    """
    def get_dimensions(self):
        """
        Returns the lengths, with, and depth of this matrix in this order
        """
        return [self.__xlength, self.__ylength, self.__zlength]


    def point_in_boarders(self, x:int, y:int, z:int) -> bool:
        """
        Returns true if the given point is within the borders of this matrix and false if not
        :param x: the x coordinate of the point to be tested
        :param y: the y coordinate of the point to be tested
        :param z: the z coordinate of the point to be tested
        """
        if x < 0 or y < 0 or z < 0:
            return False

        if self.get_dimensions()[0] >= x and self.get_dimensions()[1] >= y and self.get_dimensions()[2] >= z:
            return True
        return False
    """
    END public specific functions
    """