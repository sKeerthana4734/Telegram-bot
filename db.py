import mysql.connector
import mysql.connector as mysql
# enter your server IP address/domain name
HOST = "127.0.0.1"  # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "bot"
# this is the user you create
USER = "root"
# user password
PASSWORD = "4321"


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
