from flask import Flask, render_template, request, redirect, session
from db import get_connection

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/")
def home():
    return render_template("index.html")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        enr = request.form["enr"]
        name = request.form["name"]
        password = request.form["password"]
        rank = request.form["rank"]

        con = get_connection()
        cur = con.cursor()

        cur.execute("INSERT INTO students VALUES (%s,%s,%s,%s)",
                    (enr, name, password, rank))
        con.commit()
        con.close()

        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        enr = request.form["enr"]
        password = request.form["password"]

        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT name, stdrank FROM students WHERE enr=%s AND password=%s",
                    (enr, password))
        user = cur.fetchone()
        con.close()

        if user:
            session["name"] = user[0]
            session["rank"] = user[1]
            return redirect("/dashboard")

    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",
                           name=session["name"],
                           rank=session["rank"])

# PREDICT
@app.route("/predict")
def predict():
    rank = session["rank"]

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT institute_name, course, opening_rank, closing_rank
        FROM colleges
        WHERE %s BETWEEN opening_rank AND closing_rank
        LIMIT 10
    """, (rank,))

    data = cur.fetchall()
    con.close()

    return render_template("result.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
