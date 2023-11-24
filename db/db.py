import sqlite3
from sqlite3 import Error

class DatabaseConnection:

    def __init__(self, connection):
        self.connection = connection


    """
    Creates and returns a connection to a sqlite3 database.
    """
    def create_connection(self, path):
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        
        return connection

    
    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                self.connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)