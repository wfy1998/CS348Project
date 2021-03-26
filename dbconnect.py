import mysql.connector

# connect to your local database
def connection():
    cnx = mysql.connector.connect(user="root", password="awesomeblog",
                                  host="localhost",
                                  database="348Project")
    c = cnx.cursor()
    return cnx, c
