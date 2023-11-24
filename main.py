from barcharts import BarCharts
import sqlite3
from sqlite3 import Error

if __name__ == "__main__":

    path = "./db/nba-elo-db.db"
    try:
        connection = sqlite3.connect(path)
        connection.text_factory = str
    except Error as e:
        print("Error occurred: " + str(e))


    bc = BarCharts(connection)
    bc.displayPreAndPostSeasonEloComparison()


    connection.close()