import mysql.connector


# connect to your local database
def connection():
    cnx = mysql.connector.connect(user="root", password="qwerty12345",
                                  host="localhost",
                                  database="cs348project")
    c = cnx.cursor()
    return cnx, c