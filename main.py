from barcharts import BarCharts
import sqlite3
from sqlite3 import Error



def displayBarCharts():
    bc = BarCharts(connection)
    bc.displayBestMatchups()


if __name__ == "__main__":

    path = "./db/nba-elo-db.db"
    try:
        connection = sqlite3.connect(path)
        connection.text_factory = str
    except Error as e:
        print("Error occurred: " + str(e))


    displayBarCharts()

    connection.close()
