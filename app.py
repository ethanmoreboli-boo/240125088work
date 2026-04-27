from flask import Flask, render_template, redirect, request
import pandas as pd 
import mysql.connector
import matplotlib.pyplot as plt

app = Flask(__name__)

db = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "root",
    database = "database"
)

cursor = db.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        query = "INSERT INTO information (username, password) VALUE (%s, %s)"
        values = (username, password)

        cursor.execute(query, values)
        db.commit()

        return redirect("login")
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        
        query = "SELECT * FROM information WHERE username=%s AND password=%s"
        values = (username, password)

        cursor.execute(query, values)
        user = cursor.fetchone()  

        if user:
            return redirect("/dashboard")  
        else:
            return "INVALID DATA"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    df = pd.read_csv("Apple_data.csv")

    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    return render_template("dashboard.html", after=after, 
                           all_data=df.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)


