from dbconnect import connection
import mysql.connector
from flask import Flask, redirect, url_for, render_template, request, session, flash
import bcrypt

app = Flask(__name__)
session = {}
@app.route('/')
def home():
    cnx, c = connection()
    return render_template("home.html")

@app.route('/register', methods = ["GET","POST"])
def register():
    cnx, c = connection()
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form('name')
        email = request.form('email')
        password = request.form['password'].encode("utf-8")
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        query = "INSERT INTO user(username, email, password) VALUES " \
                 "("+str(name)+","+str(email)+","+str(password)+");"
        c.execute(query)
        cnx.commit()
                 
        session['name'] = name
        session['email'] = email
        return render_template("login.html")

@app.route('/login', methods = ["GET","POST"])
def login():
    cnx, c = connection()
    if request.method == "GET":
        return render_template("login.html")
    else:

        email = request.form('email')
        password = request.form['password'].encode("utf-8")
       
        query = "select * from user where email = " + email+";"
                 
        c.execute(query)

        user = c.fetchone()

        if len(user) > 0:
            if bcrypt.hashpw(password,user['password'].encode("utf-8")) == user['password'].encode("utf-8"):
                session['name'] = name
                session['email'] = email
                return redirect(url_for("home"))
            else:
                return "ERROR"
        else:
            return "ERROR"
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route('/profile')
def profile():
    
    return render_template("profile.html")


@app.route('/diet')
def diet():
    cnx, c = connection()
    query = "select date, type from dietRecord JOIN meal on dietRecord.meal_id = meal.meal_id;"
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
        mealtype = request.form["type"]
        month = request.form["month"]
        date = request.form["date"]
        year = request.form["year"]
        query = "INSERT INTO meal(type) VALUES ('" +str(mealtype) + "');"
        c.execute(query)

        c.execute("SELECT MAX(meal_id) FROM meal;")
        meal_id = c.fetchone()[0]
        petid = 1
        if len(month) == 1: month="0"+month
        if len(date) == 1: date = "0"+date
        datetime = month+"/"+date+"/"+year

        query2 = "INSERT INTO dietRecord(pet_id, meal_id, date) VALUES " \
                 "("+str(petid)+","+str(meal_id)+",'"+datetime+"');"
        c.execute(query2)

        c.close()
        cnx.commit()
        cnx.close()
        return redirect(url_for("diet"))

if __name__ == '__main__':
   app.run(debug=True)