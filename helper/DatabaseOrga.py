from core.ClassType import ClassType
from database.Database import Database



def reset_db_tables():
    """
        WARNING: ALL DATA IN TrainControl WILL BE LOST!
        Resets all the tables given in ClassType enum from the database and creates them new,
        tables that are not within this enum have to be deleted manually to allow TrainControl to run
        WARNING: ALL DATA IN TrainControl WILL BE LOST!
    """
    Database.connect()
    delete_all_tables()
    for enum in ClassType:
        query_string = (str(enum).replace("ClassType.", "").lower())
        query_string = query_string + "(oid VARCHAR(10)"
        for i in range(2, enum.value.__len__()):
            query_string = query_string + ", " + enum.value[i][0] + " "

            match enum.value[i][1]:
                case "boolean":
                    query_string = query_string + "BOOLEAN"
                case "str":
                    query_string = query_string + "VARCHAR"
                case "numeric":
                    query_string = query_string + "NUMERIC"
                case "integer":
                    query_string = query_string + "INTEGER"
                case "date":
                    query_string = query_string + "DATE"
                case _:
                    raise Exception("Table reset failed, one of the types for the table columns was not str, numeric, integer or date")


        query_string = query_string + ")"
        Database.run_sql_query("CREATE TABLE " + query_string,False)
        print("Table " + (str(enum).replace("ClassType.", "").lower() + " created"))
    print("All tables created")



def delete_all_tables():
    """
        WARNING: ALL DATA IN TrainControl WILL BE LOST!
        Resets all the tables given in ClassType enum from the database
        WARNING: ALL DATA IN TrainControl WILL BE LOST!
    """
    tables_to_drop = Database.run_sql_query("""
                    SELECT table_name FROM INFORMATION_SCHEMA.TABLES
                        WHERE TABLE_SCHEMA = 'public'
                """)

    if len(tables_to_drop) == 0:
        return

    tables_to_drop_string = ""
    for table_to_drop in tables_to_drop:
        tables_to_drop_string = tables_to_drop_string + table_to_drop + ", "

    tables_to_drop_string = tables_to_drop_string[0:tables_to_drop_string.__len__() -2]
    Database.connect()
    Database.run_sql_query("DROP TABLE " + tables_to_drop_string, False)
    print("All tables dropped")


#reset_db_tables()