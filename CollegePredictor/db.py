import mysql.connector

def get_connection():
    return mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ChintuProject",
            auth_plugin="mysql_native_password"
        )
