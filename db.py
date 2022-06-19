import mysql.connector
import mysql.connector as mysql
# enter your server IP address/domain name
HOST = "sql6.freesqldatabase.com"  # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "sql6500863"
# this is the user you create
USER = "sql6500863"
# user password
PASSWORD = "63b5KvKT27"


def connect():
    try:
        db_connection = mysql.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD, connection_timeout=60000)
        print("Connected to:", db_connection.get_server_info())
        return db_connection

    except mysql.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
