from dbconnect import connection
import mysql.connector
from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)

@app.route('/diet')
def show_diet():
    cnx, c = connection()
    query = "select * from meal;"
    c.execute(query)

    data = c.fetchall()
    c.close()
    cnx.close()
    return render_template("diet.html", data=data)

@app.route('/addmeal', methods=["GET","POST"])
def addmeal():
    cnx, c = connection()
    if request.method == "GET":
        return render_template("addmeal.html")
    else:
        name = request.form.get("Food Name")
        amount = request.form.get("amount")
        query1 = "SELECT food_id from food where name ==" + name;
        c.execute(query1)
        id = c.fetchall()
        query2 = "INSERT INTO mealrel (meal_id, food_id, amount) VALUES (1,"+ id[0] +","+ name+");"


if __name__ == '__main__':
   app.run()