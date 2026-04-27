from flask import Flask, render_template, redirect, request
import pandas as pd 
import mysql.connector
import matplotlib.pyplot as plt
import os

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

    df = df.drop_duplicates()

    if not os.path.exists('static'):
        os.makedirs('static')

    products = df['Product'].unique()
    years = ['Year1_kWh', 'Year2_kWh', 'Year3_kWh', 'Year4_kWh', 'Year5_kWh']

    plt.figure(figsize=(10,5))
    for product in products:
        subset = df[df['Product'] == product]
        avg_kwh = subset[years].mean()
        plt.plot([1,2,3,4,5], avg_kwh, marker='o', label=product)

    plt.title("Average kWh Consumption Over 5 Years by Product")
    plt.xlabel("Year After Purchase")
    plt.ylabel("kWh")
    plt.xticks([1,2,3,4,5])
    plt.legend()
    plt.grid(True)

    plt.savefig("static/plot.png")
    plt.close() 

    df['Total_kWh'] = df[years].sum(axis=1)
    bar_plot = df.groupby('Product')['Total_kWh'].sum().plot(kind='bar', figsize=(10,5))
    plt.title("Total kWh Consumption per Product")
    plt.ylabel("Total kWh")
    plt.tight_layout()
    plt.savefig("static/bar.png")
    plt.close()

    return render_template("dashboard.html", all_data=df.to_dict(orient='records'))


if __name__ == "__main__":
    app.run(debug=True)


