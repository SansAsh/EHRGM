import mysql.connector
from mysql.connector import Error as MySQLError

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ehrgm',
            user='root',
            password=''
        )
        return connection

    except MySQLError as e:
        print("Erreur connexion BDD:", e)
        return None