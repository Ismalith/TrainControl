import os
from configparser import ConfigParser
from core.Exceptions import IniReadException


class Tools:
    @classmethod
    def ini_reader(cls, path:str, filename:str, section:str):
        """
        Reader that turns the data from .ini files into a dict, it returns all given parameters in a group as a dict,
            the parameter group is the title in the [ ] brackets
        :param path: the path from the folder "TrainControl" to the .ini file
        :param filename: the name of the file itself, slashes in any way are not required and should be avoided the reader can however compensate slashes to some degree
        :param section: the parameter group that is to be read, the parameter group is the title in the [ ] brackets
        """
        filename = filename.replace("/", "")
        path = path.replace("/", "\\")
        path = path.removesuffix("\\")
        path = path.removeprefix("\\")
        file_with_path = os.path.abspath(__file__).removesuffix("core\\Tools.py") + path + "\\" + filename

        parser = ConfigParser()
        parser.read(file_with_path)

        config_dict = {}
        if parser.has_section(section):
            parser.has_section(section)
            params = parser.items(section)
            for param in params:
                config_dict[param[0]] = param[1]
        else:
            raise IniReadException("Section {0} not found in the {1} file".format(section, filename))
        return config_dict
