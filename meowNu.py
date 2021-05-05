from dbconnect import connection
import mysql.connector
from flask import Flask, redirect, url_for, render_template, request, session, flash
import bcrypt
import datetime

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
        if user != None:
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


@app.route('/profile', methods=["GET", "POST"])
def profile():
    cnx, c = connection()

    if request.method == "GET":
        query = "select username, email, gender, age, city from user where email = \"" + session['email'] + "\";"
        c.execute(query)
        data = c.fetchall()
        c.close()
        cnx.close()
        return render_template("profile.html", data=data)
    else:
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        city = request.form['city']

        query = "Update user set username = %s, gender = %s, age = %s, city = %s where email = %s", (
            name, gender, age, city, session['email'])
        c.execute(query)
        c.close()
        cnx.commit()
        cnx.close()

        return render_template("profile.html")

@app.route('/pets', methods=["GET", "POST"])
def pets():
    cnx, c = connection()
    email = session['email']
    if request.method == "GET":

        c.execute("SELECT user_id FROM user WHERE email = " + email)
        user = 0
        for uid in c:
            user = uid

        query = "SELECT pet_id, name"
        query += "FROM pet"
        query += "WHERE user_id = " + str(user)

        c.execute(query)

        data = c.fetchall()

        c.close()
        cnx.close()
        return render_template("pets.html", data=data)

    else:
        name = request.form["pet_name"]
        species = request.form["species"]
        age = request.form["pet_age"]
        weight = request.form["weight"]
        status = request.form["status"]

        record = [name, species, age, weight, status]
        c.execute("INSERT INTO pet(name, species, age, weight, status) VALUES(%s, %s, %s, %s, %s)", record)

        c.close()
        cnx.commit()
        cnx.close()
        return redirect(url_for("pets"))


@app.route('/pets_detail')
def pets_detail():
    cnx, c = connection()

    pet_id = request.GET.get('pet_id')

    query = "SELECT pet_id, name, species, age, weight, status"
    query += "FROM pet WHERE pet_id = " + str(pet_id) + ";"
    c.execute(query)

    data = c.fetchall()

    c.close()
    cnx.close()
    return render_template("pets_detail.html", data=data)


@app.route('/pets_daily_report')
def pets_daily_report():
    cnx, c = connection()
    pet_id = request.GET.get('pet_id')

    q = "SELECT name FROM pet WHERE pet_id = " + pet_id;
    c.execute(q)
    name = c.fetchall()

    query = "SELECT date, SUM(amount * calories)"
    query += "FROM dietrecord"
    query += "JOIN mealrel ON dietrecord.meal_id = mealrel.meal_id"
    query += "JOIN food ON mealrel.food_id = food.food_id"
    query += "WHERE dietrecord.pet_id = 1"
    query += "GROUP BY date"

    c.execute(query)

    cur = datetime.date.today()
    year_now, week_now, day_now = cur.isocalendar()

    data = {name}
    for (date, cal) in c:
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
        week = d.isocalendar()[1]
        if week == week_now:
            data += (date, cal)

    c.close()
    cnx.close()
    return render_template("pets_daily_report.html", data=data)

@app.route('/diet',methods=["GET","POST"])
def diet():
    cnx, c = connection()
    query = "select meal.meal_id, date, type from dietRecord JOIN meal on dietRecord.meal_id = meal.meal_id;"
    c.execute(query)
    data = c.fetchall()

    info =[]
    for item in data:
        meal_id = item[0]
        query = "select SUM(amount*calories/100) from (select meal_id, calories, amount " \
                "from mealrel join food on mealrel.food_id=food.food_id) as a " \
                "where meal_id = %s;"
        c.execute(query,(meal_id,))
        total = c.fetchone()[0]
        new =item + (total,)
        info.append(new)


    c.close()
    cnx.close()

    return render_template("diet.html", info=info)

@app.route('/addmeal', methods=["GET","POST"])
def addmeal():
    cnx, c = connection()
    if request.method == "GET":
        c.execute("SELECT name from food;")
        foodlist = [foodlist[0] for foodlist in c.fetchall()]
        foodlist.append("null")
        return render_template("addmeal.html", foodlist = foodlist)
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

        petid = 1
        if len(month) == 1: month="0"+month
        if len(date) == 1: date = "0"+date
        datetime = month+"/"+date+"/"+year

        query2 = "INSERT INTO dietRecord(pet_id, meal_id, date) VALUES (%s,%s,%s);"
        c.execute(query2, (petid, meal_id, datetime))

        c.close()
        cnx.commit()
        cnx.close()
        return redirect(url_for("diet"))

@app.route('/viewmeal', methods=["GET","POST"])
def viewmeal():
    cnx, c = connection()
    meal_id = request.form.get("meal_id")

    data=[]
    c.execute("select date from dietRecord where meal_id=%s",(meal_id,))
    date = c.fetchone()[0]
    data.append(date)

    c.execute("select type from meal where meal_id=%s",(meal_id,))
    type = c.fetchone()[0]
    data.append(type)

    c.execute("select name, amount, calories, moisture, protein, lipid "
              "from mealrel join food on mealrel.food_id = food.food_id "
              "where meal_id=%s;", (meal_id,))
    food = c.fetchall()

    info = []
    total = 0
    for item in food:
        temp = item[1]* item[2] / 100
        new = item + (temp,)
        info.append(new)
        total += temp

    c.close()
    cnx.commit()
    cnx.close()
    return render_template("viewmeal.html", data=data, info=info, total=total)


if __name__ == '__main__':
    app.secret_key = "012#!ApaAjaBoleh)(*^%"
    app.run(debug=True)
