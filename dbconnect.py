import mysql.connector


# connect to your local database
def connection():
    cnx = mysql.connector.connect(user="root", password="991110",
                                  host="localhost",
                                  database="project")
    c = cnx.cursor()
    return cnx, c
