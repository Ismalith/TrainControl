import psycopg

from database import Database

database = psycopg.connect("host=" + dbconnection.DATABASEHOST
                           + "post=" + dbconnection.DATABASEPORT
                           + "dbname=" + dbconnection.DATABASENAME)
database.
connection = sqlalchemy.create_engine('postgresql://database:xtnpaz@192.168.178.66:22/database').connect()
connection.close()

#class SQLCore:
 #   def connect(self):












with SSHTunnelForwarder(
    (DATABASEHOST, 22),
    ssh_username=DATABASEUSER,
    ssh_password=DATABASEPASSWORT,
    remote_bind_address=(DATABASEHOST, DATABASEPORT)) as server:

    server.start()
    print("server connected")

    params = {
        'dbname': DATABASENAME,
        'user': DATABASEUSER,
        'password': DATABASEPASSWORT,
        'host': DATABASEHOST,
        'port': 22,
        'sslmode': 'disable'
    }

conn = psycopg.connect(**params)
curs = conn.cursor()
print("database connected")