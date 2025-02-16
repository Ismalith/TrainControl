import inspect
from typing import override
import numpy as np
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadInitializationException
from database.Database import Database
from matrix.Matrix import Matrix


class Plane(ClassBase):
    """
    Matrix

    A plane that contains the actual objects of a track like rails and signals
    """
    __matrix:Matrix
    __xlength:int
    __ylength:int
    __xpos:int
    __ypos: int
    __zpos: int
    __xrot:int
    __yrot: int
    __zrot: int



    """
    START create functions
    """
    def __init__(self, name:str, xlength:int, ylength:int, xpos:int, ypos:int, zpos:int, xrot:int, yrot:int, zrot:int, matrix:Matrix = None, oid:str = None):
        """
        Initialize the Plane, do not use manually
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
            super().__init__(ClassType.PLANE, name, oid)
        else:
            super().__init__(ClassType.PLANE, name)

        self.__matrix = matrix
        self.__xlength = xlength
        self.__ylength = ylength
        self.__xpos = xpos
        self.__ypos = ypos
        self.__zpos = zpos
        self.__xrot = xrot
        self.__yrot = yrot
        self.__zrot = zrot
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
        Puts the given parameter in this Plane object, only to be used by the database to load an already existing plane
        from the database, to create a new plane, use the constructor directly and NEVER set the parameter "oid"
        :return: the Plane object with the given parameter
        """
        new_plane = object.__new__(cls)
        new_plane.__init__(data[1], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[2], data[0])
        return new_plane


    @override
    def __db_write_to_db__(self):
        dimensions = self.get_dimensions()
        position = self.get_position()
        rotation = self.get_rotation()
        sql_insert = ("INSERT INTO plane (oid, name, matrix, xlength, ylength, xpos, ypos, zpos, xrot, yrot, zrot) VALUES ('"
                      + self.get_oid() + "','" + self.get_name() + "','" + str(self.get_matrix().get_oid()) + "','" +
                      str(dimensions[0]) + "','" + str(dimensions[1]) + "','" +
                      str(position[0]) + "','" + str(position[1]) + "','" + str(position[2]) + "','" +
                      str(rotation[0]) + "','" + str(rotation[1]) + "','" + str(rotation[2]) + "')")
        Database.run_sql_query(sql_insert, False)
    """
    END db functions
    """



    """
    START public general functions
    """
    @classmethod
    def create_new(cls, name:str, xlength:int = 0, ylength:int = 0, xpos:int = -1, ypos:int = -1, zpos:int = 0, xrot:int = 0, yrot:int = 0, zrot:int = 0, ):
        """
        Creation methode to create and write a new plane to the database, only create new lane with this method, the matrix is added automatically if one exists,
        if none exists the plane can itself be the base object however this only allowes one plane and a matrix can not be added after the fact
        :param name: the name for the plane, if not chosen manually the new relay will get the name "Plane 1"
        :param xlength: the length of the plane in µm (1/10000)
        :param ylength: the width of the plane in µm (1/10000)
        :param xpos: the x position of the center of the plane in the matrix in µm (1/10000)
        :param ypos: the y position of the center of the plane in the matrix in µm (1/10000)
        :param zpos: the horizontal position of the center of the plane in the matrix in µm (1/10000)
        :param xrot: the rotation around the x-axis of the center of the plane in the matrix in µm (1/10000)
        :param yrot: the rotation around the y-axis of the center of the plane in the matrix in µm (1/10000)
        :param zrot: the rotation around the z-axis of the center of the plane in the matrix in µm (1/10000)
        :return: the newly created plane
        """
        if name is None:
            highest_generic_name = Database.run_sql_query("SELECT name FROM plane WHERE name ~ '^plane \\d+$' ORDER BY name DESC LIMIT 1")
            name = "Plane " + str(int(str(highest_generic_name).rsplit(" ")[1]) + 1)
        else:
            found_planes = Database.run_sql_query("SELECT count(oid) FROM plane WHERE name = '" + name + "'")
            if found_planes > 0:
                raise BadInitializationException("A planes pie with the name " + name + " is already in the database")


        if xlength < 0 or ylength < 0:
            raise BadInitializationException("There was an attempt to create a new Plane object with one of it's dimensions smaller than 1:\n"
                                             "X length = " + str(xlength) + "\n"
                                             "z length = " + str(ylength) + "\n")

        if xpos < -1 or ypos < -1 or zpos < 0:
            raise BadInitializationException("There was an attempt to create a new Plane object with a starting point with negative coordinates:\n"
                                             "X pos = " + str(xpos) + "\n"
                                             "Y pos = " + str(ypos) + "\n"
                                             "Z pos = " + str(zpos) + "\n")

        if xrot < -90 or yrot < -360 or zrot < -90:
            raise BadInitializationException("There was an attempt to create a new Plane object with a rotation outside of the negative rotation limits:\n"
                                             "The rotation limits are x = -90°, y = -360°, z = -90°:\n"
                                             "X rotation = " + str(xrot) + "\n"
                                             "Y rotation = " + str(yrot) + "\n"
                                             "Z rotation = " + str(zrot) + "\n")

        if xrot > 90 or yrot > 90 or zrot > 359:
            raise BadInitializationException("There was an attempt to create a new Plane object with a rotation outside of the rotation limits\n"
                                             "The rotation limits are x = 90°, y = 90°, z = 359°:\n"
                                             "X rotation = " + str(xrot) + "\n"
                                             "Y rotation = " + str(yrot) + "\n"
                                             "Z rotation = " + str(zrot) + "\n")


        matrix:Matrix = Database.get_object_for_oid(Database.run_sql_query("SELECT oid FROM matrix"))

        if matrix is None:
            if xpos == -1 and ypos == -1 and ypos == -1 and xrot == 0 and yrot == 0 and zrot == 0:
                new_plane = object.__new__(cls)
                new_plane.__init__(name, xlength, ylength, xpos, ypos, zpos, xrot, yrot, zrot, None)
                return  new_plane
            else:
                raise BadInitializationException("There was an attempt to create a plane that hat rotation or position values given while there was not matrix defined, "
                                                 "to define a plane without a matrix position and rotation parameter must be empty, "
                                                 "if the plane should be within a matrix the matrix needs to be created first.")

        if xlength == 0:
            xlength = matrix.get_dimensions()[0]

        if ylength == 0:
            ylength = matrix.get_dimensions()[1]

        if xpos == -1:
            xpos = matrix.get_dimensions()[0] / 2

        if ypos == -1:
            ypos = matrix.get_dimensions()[1] / 2


        corner_1 = [0, 0]
        corner_2 = [xlength, 0]
        corner_3 = [0, ylength]
        corner_4 = [xlength, ylength]
        four_corners = [corner_1, corner_2, corner_3, corner_4]

        for corner in four_corners:
            absolute_point = Plane.__get_absolute_position(corner[0], corner[1], xpos, ypos, zpos, xrot, yrot, zrot)
            if absolute_point[0] < 0 or absolute_point[1] < 0 or absolute_point[2] < 0:
                raise BadInitializationException("Attempt to create a new plane with at least one point outside the matrix, found point:\n" +
                                                 str(corner[0]) + "|" + str(corner[1]) + " (" + str(absolute_point[0]) + "|" + str(absolute_point[1]) + "|" + str(absolute_point[2]) + ")")

        new_plane = object.__new__(cls)
        new_plane.__init__(name, xlength, ylength, xpos, ypos, zpos, xrot, yrot, zrot, matrix)
        return new_plane


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
    START private specific functions
    """
    @classmethod
    def __get_absolute_position(cls, x:int, y:int, xpos:int, ypos:int, zpos:int, xrot:int = 0, yrot:int = 0, zrot:int = 0):
        x = float(x)
        y = float(y)
        xpos = float(xpos)
        ypos = float(ypos)
        zpos = float(zpos)
        xrot = float(xrot)
        yrot = float(yrot)
        zrot = float(zrot)

        xrad = np.radians(xrot)
        yrad = np.radians(yrot)
        zrad = np.radians(zrot)
        point = np.array([float(x), float(y), 0.0])

        rot_matrix_x = np.array([
            [1, 0, 0],
            [0, np.cos(xrad), -np.sin(xrad)],
            [0, np.sin(xrad), np.cos(xrad)]
        ])

        rot_matrix_y = np.array([
            [np.cos(yrad), 0, -np.sin(yrad)],
            [0, 1, 0],
            [np.sin(yrad), 0, np.cos(yrad)]
        ])

        rot_matrix_z = np.array([
            [np.cos(zrad), -np.sin(zrad), 0],
            [np.sin(zrad), np.cos(zrad), 0],
            [0, 0, 1]
        ])

        rot_point = rot_matrix_z @ (rot_matrix_y @ (rot_matrix_x @ point))
        return [rot_point[0] + float(xpos), rot_point[1] + float(ypos), rot_point[2] + float(zpos)]
    """
    END private specific functions
    """



    """
    START public specific functions
    """
    def get_matrix(self):
        """
        Returns the matrix in which this plane is
        """
        return self.__matrix


    def get_dimensions(self):
        """
        Returns the x and z dimensions for this plane
        """
        return [self.__xlength, self.__ylength]


    def get_position(self):
        """
        Returns the x, y and z position of this plane in the matrix, the point returned is the center of the plane
        """
        return [self.__xpos, self.__ypos, self.__zpos]


    def get_rotation(self):
        """
        Returns the x, y and z rotation of this plane in the matrix, the rotation point returned is in the center of the plane
        """
        return [self.__xrot, self.__yrot, self.__zrot]


    def get_absolute_position(self, x:int, y:int):
        """
        Returns the absolute position in the matrix for the given point on the plane
        """
        return Plane.__get_absolute_position(x, y, self.__xpos, self.__ypos, self.__zpos, self.__xrot, self.__yrot, self.__zrot)
    """
    END public specific functions
    """