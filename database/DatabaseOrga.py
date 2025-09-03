from core.ClassType import ClassType
from core.Exceptions import DBOrgaException
from database.Database import Database



def reset_db_tables():
    """
        WARNING: ALL DATA IN TrainControl WILL BE LOST!
        Resets all the tables given in ClassType enum from the database and creates them new,
        tables that are not within this enum have to be deleted manually to allow TrainControl to run
        WARNING: ALL DATA IN TrainControl WILL BE LOST!
    """
    delete_all_tables()
    for enum in ClassType:
        query_string = (str(enum).replace("ClassType.", "").lower())
        query_string = query_string + "(oid VARCHAR(10) NOT NULL UNIQUE"
        for i in range(2, enum.value.__len__()):
            query_string = query_string + ", " + enum.value[i][0] + " "

            if enum.value[i].__len__() == 1:
                found = False
                for item in ClassType:
                    if str(enum.value[i][0]).upper() in str(item.name):
                        query_string = query_string + "VARCHAR"
                        found = True
                        break

                if found:
                    continue
                else:
                    delete_all_tables()
                    raise DBOrgaException("Table reset failed, one of the columns only had one value, this is only allowed if the column \n"
                        " contains the oids to another table, which also wasn't found, make sure, all columns have \n"
                        " their type and the table names to other tables are written correctly, \n"
                        " Found bad column name: " + (enum.value[i][0]).upper())


            match enum.value[i][1]:
                case "boolean":
                    query_string = query_string + "BOOLEAN"
                case "string":
                    query_string = query_string + "VARCHAR"
                case "numeric":
                    query_string = query_string + "NUMERIC"
                case "integer":
                    query_string = query_string + "INTEGER"
                case "date":
                    query_string = query_string + "DATE"
                case _:
                    raise DBOrgaException("Table reset failed, one of the types for the table columns was not string, numeric, integer or date\n"
                                          "Failed table: " + str(enum).replace("ClassType.", "") + "\n"
                                          "Failed parameter: " + enum.value[i][0] + " with " + enum.value[i][1])


        query_string = query_string + ")"
        Database.run_sql_query("CREATE TABLE " + query_string,False)
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
    print(tables_to_drop)

    if tables_to_drop is None or len(tables_to_drop) == 0:
        return

    if not isinstance(tables_to_drop, str):
        tables_to_drop_string = ""
        for table_to_drop in tables_to_drop:
            tables_to_drop_string = tables_to_drop_string + table_to_drop + ", "

        tables_to_drop_string = tables_to_drop_string[0:tables_to_drop_string.__len__() - 2]

    else:
        tables_to_drop_string = tables_to_drop

    print("DROP TABLE " + tables_to_drop_string)
    Database.run_sql_query("DROP TABLE " + tables_to_drop_string, False)
    print("All tables dropped")