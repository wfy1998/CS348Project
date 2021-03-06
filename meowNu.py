from dbconnect import connection
import mysql.connector
from flask import Flask, redirect, url_for, render_template, request, session, flash
import bcrypt
import datetime
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def home():
    cnx, c = connection()
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    cnx, c = connection()
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        if 'email' in session:
            if str(email) in session['email']:
                return render_template("error.html")
        psw = request.form['psw'].encode("utf-8")
        hash_password = bcrypt.hashpw(psw, bcrypt.gensalt())
        c.execute("INSERT INTO user(username, email, password) VALUES (%s,%s,%s)", (name, email, hash_password,))
        c.close()
        cnx.commit()
        cnx.close()

        session['name'] = name
        session['email'] = email
        return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    cnx, c = connection()
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form['email']
        password = request.form['password'].encode("utf-8")

        query = "select * from user where email = \"" + email + "\";"
        c.execute(query)

        user = c.fetchone()
        print(user)
        print("\n\n\n")
        # c.close()
        # cnx.close()
        if user is not None:
            if bcrypt.hashpw(password, user[2].encode("utf-8")) == user[2].encode("utf-8"):
                session['name'] = user[1]
                session['email'] = email
                return redirect(url_for("home"))
            else:
                return render_template("error.html")
        else:
            return render_template("error.html")
        return redirect(url_for("home"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route('/profile')
def profile():
    cnx, c = connection()
    user_id = request.args.get('user_id')
    args = []
    args.append(str(session['email']))
    c.callproc("getUserInfo1", args)
    food = []
    for result in c.stored_results():
        data = result.fetchall()

    c.close()
    cnx.commit()
    cnx.close()
    return render_template("profile.html", data=data)


@app.route('/setProfile', methods=["GET", "POST"])
def setProfile():
    cnx, c = connection()

    if request.method == "GET":
        return render_template("setProfile.html")
    else:
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        city = request.form['city']

        query = "update user set username = %s, gender = %s, age = %s, city = %s where email = %s"
        c.execute(query, (name, gender, age, city, session['email']))

        c.close()
        cnx.commit()
        cnx.close()

        return redirect(url_for("profile"))


@app.route('/user', methods=["GET", "POST"])
def user():
    cnx, c = connection()
    if request.method == "GET":
        return render_template("user.html")
    else:
        city = request.form['city']
        query = "select username, email, gender, age, city from user" \
                " where email in (select email from user where city = \"" + city + "\"); "
        c.execute(query)
        data = c.fetchall()
        c.close()
        cnx.commit()
        cnx.close()
        return render_template("user.html", data=data)


@app.route('/pets', methods=["GET", "POST"])
def pets():
    cnx, c = connection()
    c = cnx.cursor(buffered=True)
    email = session['email']

    # email = "123@gmail.com"
    c.execute("SELECT user_id FROM user WHERE email = '%s'" % (email,))
    user = c.fetchone()

    print("User: " + str(user[0]))

    if request.method == "GET":

        c.execute("SELECT pet_id, name FROM pet WHERE user_id = %s" % (user[0],))

        data = c.fetchall()

        # if data is None:
        #     data = {}

        print("SELECT pet_id, name FROM pet WHERE user_id = " + str(user[0]) + "\n" + str(data) + "\n\n")

        c.close()
        cnx.close()
        return render_template("pets.html", data=data)

    else:
        name = request.form["pet_name"]
        species = request.form["species"]
        age = request.form["pet_age"]
        gender = request.form["pet_gender"]
        weight = request.form["weight"]
        status = request.form["status"]

        print((user, name, species, age, gender, weight, status,))

        c.execute("""
                    INSERT INTO pet(user_id, name, species, age, gender, weight, status) 
                    VALUES(%s, '%s', '%s', %s, '%s', %s, '%s')""" % (
            user[0], name, species, age, gender, weight, status,))

        c.close()
        cnx.commit()
        cnx.close()
        return redirect(url_for("pets"))


@app.route('/pets_detail')
def pets_detail():
    cnx, c = connection()

    pet_id = request.args.get('pet_id')

    c.execute("SELECT pet_id, name, species, age, weight, status FROM pet WHERE pet_id = %s" % (pet_id,))

    data = c.fetchone()

    print("SELECT pet_id, name, species, age, weight, status FROM pet WHERE pet_id = " + str(pet_id) + "\n" + str(
        data) + "\n\n")

    c.close()
    cnx.close()
    return render_template("pets_detail.html", data=data)


@app.route('/pets_daily_report')
def pets_daily_report():
    cnx, c = connection()
    pet_id = request.args.get('pet_id')

    print(str(pet_id))

    c.execute("SELECT name FROM pet WHERE pet_id = %s" % (pet_id,))
    name = c.fetchone()

    print(str(name[0]) + "\n\n")

    cur = datetime.date.today()
    year_now, week_now, day_now = cur.isocalendar()

    args = [cur.strftime('%m/%d/%Y'), pet_id]
    c.callproc("GetTodaysDiet", args)

    today_diet = []
    for result in c.stored_results():
        today_diet = result.fetchall()

    print("week now:" + str(week_now))

    c.callproc("GetWeeklyDiet", [pet_id])

    weeklydiet = []
    for result in c.stored_results():
        weeklydiet = result.fetchall()

    dates = []
    cals = []
    for (date, cal) in weeklydiet:
        print("date: " + str(date) + " cal: " + str(cal))
        d = datetime.datetime.strptime(date, '%m/%d/%Y')
        week = d.isocalendar()[1]
        print("week: " + str(week))
        if week == week_now:
            dates.append(date)
            cals.append(cal)

    print("dates: " + str(dates))
    print("cals: " + str(cals) + "\n\n")

    c.close()
    cnx.close()
    return render_template("pets_daily_report.html", name=name, dates=dates, cals=cals, today_diet=today_diet)


@app.route('/diet', methods=["GET", "POST"])
def diet():
    cnx, c = connection()
    pet_id = request.args.get('pet_id')
    c.execute("select name from pet where pet_id=%s", (pet_id,))
    pet_name = c.fetchone()[0]

    query = "select meal.meal_id, date, type " \
            "from dietRecord JOIN meal on dietRecord.meal_id = meal.meal_id where pet_id=%s;"
    c.execute(query, (pet_id,))
    data = c.fetchall()

    info = []
    for item in data:
        meal_id = item[0]
        query = "select SUM(amount*calories/100) from (select meal_id, calories, amount " \
                "from mealrel join food on mealrel.food_id=food.food_id) as a " \
                "where meal_id = %s;"
        c.execute(query, (meal_id,))
        total = c.fetchone()[0]
        new = item + (total,)
        info.append(new)

    args = []
    args.append(pet_id)
    c.callproc("statis", args)
    statis = []
    for result in c.stored_results():
        statis = result.fetchall()

    c.close()
    cnx.close()
    return render_template("diet.html", info=info, pet_id=pet_id, pet_name=pet_name, statis=statis)


@app.route('/addmeal', methods=["GET", "POST"])
def addmeal():
    cnx, c = connection()
    pet_id = request.args.get('pet_id')

    if request.method == "GET":
        c.execute("SELECT name from food;")
        foodlist = [foodlist[0] for foodlist in c.fetchall()]
        foodlist.append("null")
        return render_template("addmeal.html", foodlist=foodlist, pet_id=pet_id)
    else:
        mealtype = request.form["type"]
        month = request.form["month"]
        date = request.form["date"]
        year = request.form["year"]
        food1 = request.form["food1"]
        amount1 = request.form["amount1"]
        food2 = request.form["food2"]
        amount2 = request.form["amount1"]
        food3 = request.form["food3"]
        amount3 = request.form["amount1"]

        food1_id = 0
        food2_id = 0
        food3_id = 0
        if food1 != "null":
            c.execute("SELECT food_id FROM food where food.name=%s;", (food1,))
            food1_id = c.fetchone()[0]

        if food2 != "null":
            c.execute("SELECT food_id FROM food where food.name=%s;", (food2,))
            food2_id = c.fetchone()[0]

        if food3 != "null":
            c.execute("SELECT food_id FROM food where food.name=%s;", (food3,))
            food3_id = c.fetchone()[0]

        query = "INSERT INTO meal(type) VALUES (%s)"
        c.execute(query, (mealtype,))

        c.execute("SELECT MAX(meal_id) FROM meal;")
        meal_id = c.fetchone()[0]
        if food1_id != 0:
            c.execute("INSERT INTO mealrel(meal_id, food_id, amount) VALUES (%s, %s, %s)",
                      (meal_id, food1_id, amount1))

        if food2_id != 0:
            c.execute("INSERT INTO mealrel(meal_id, food_id, amount) VALUES (%s, %s, %s)",
                      (meal_id, food2_id, amount2))

        if food3_id != 0:
            c.execute("INSERT INTO mealrel(meal_id, food_id, amount) VALUES (%s, %s, %s)",
                      (meal_id, food3_id, amount3))

        if len(month) == 1: month = "0" + month
        if len(date) == 1: date = "0" + date
        datetime = month + "/" + date + "/" + year

        query2 = "INSERT INTO dietRecord(pet_id, meal_id, date) VALUES (%s,%s,%s);"
        c.execute(query2, (pet_id, meal_id, datetime))

        c.close()
        cnx.commit()
        cnx.close()
        return redirect(url_for("diet", pet_id=pet_id))


@app.route('/viewmeal', methods=["GET", "POST"])
def viewmeal():
    cnx, c = connection()
    pet_id = request.args.get('pet_id')
    meal_id = request.form.get("meal_id")

    data = []
    c.execute("select date from dietRecord where meal_id=%s", (meal_id,))
    date = c.fetchone()[0]
    data.append(date)

    c.execute("select type from meal where meal_id=%s", (meal_id,))
    type = c.fetchone()[0]
    data.append(type)

    args = []
    args.append(meal_id)
    c.callproc("getView", args)
    food = []
    for result in c.stored_results():
        food = result.fetchall()

    info = []
    total = 0
    for item in food:
        temp = item[1] * item[2] / 100
        new = item + (temp,)
        info.append(new)
        total += temp

    c.close()
    cnx.commit()
    cnx.close()
    return render_template("viewmeal.html", data=data, info=info, total=total, pet_id=pet_id)


if __name__ == '__main__':
    app.secret_key = "012#!ApaAjaBoleh)(*^%"
    app.run(debug=True)
