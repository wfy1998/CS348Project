from dbconnect import connection
import mysql.connector
from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)

@app.route('/diet',methods=["GET","POST"])
def diet():
    cnx, c = connection()
    query = "select meal.meal_id, date, type from dietRecord JOIN meal on dietRecord.meal_id = meal.meal_id;"
    c.execute(query)
    data = c.fetchall()

    info =[]
    for item in data:
        meal_id = item[0]
        c.execute("select food_id, amount from mealrel where meal_id=%s;",(meal_id,))
        food = c.fetchall()
        total =0
        for i in food:
            c.execute("select calories from food where food_id=%s;", (i[0],))
            temp = c.fetchone()[0]
            total = total + temp * i[1]/100

        new =item + (total,)
        info.append(new)

    #print(info)

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

        query2 = "INSERT INTO dietRecord(pet_id, meal_id, date) VALUES " \
                 "(%s,%s,%s);"
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
   app.run()