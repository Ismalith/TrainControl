from core.ClassType import ClassType
from core.Exceptions import StartupException
from database.Database import Database

class Startup:

    @staticmethod
    def startup_db_check():
        """
        The pre run check procedure to make sure everything is ready to start TrainControl
        :return:
        """
        print(" 0% Starting...")
        print(" 0% Get table names from database...")
        responses = Database.run_sql_query("""
                        SELECT table_name FROM INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'public'
                    """)

        clean_responses = []
        for response in responses:
            clean_responses.append(str.upper(response[0]))
        print("30% received table names from database")
        print("30% check if all table names and enums exist...")

        missing_tables = []
        for enum in ClassType:
            if clean_responses.__contains__(enum.name):
                clean_responses.remove(enum.name)
            else:
                missing_tables.append(enum)


        if clean_responses.__len__() > 0:
            missing_responses_string = ""
            for response in clean_responses:
                missing_responses_string = missing_responses_string + response + ", "
            raise StartupException("The following tables where found that are not in TrainControl, make sure all tables are in TrainControl: "
                                    + missing_responses_string +
                                    "to have them in the project they need to be set in the ClassType enum")

        if missing_tables.__len__() > 0:
            missing_tables_string = ""
            for missing_table in missing_tables:
                missing_tables_string = missing_tables_string + str(missing_table).replace("ClassType.", "") + ", "
            raise StartupException("The following tables where missing in the database, make sure all tables are in the database: "
                                    + missing_tables_string +
                                    "without the tables the project can't run")

        print("50% All table names and enums where found")
        return True

    @staticmethod
    def startup_hardware_check():
        return True

    @staticmethod
    def start():
        return True
