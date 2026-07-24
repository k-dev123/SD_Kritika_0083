from flask import Flask, render_template, request, redirect, url_for
from database import get_connection

app = Flask(__name__)


# -------------------------
# Home Page
# -------------------------
@app.route("/")
def home():
    return redirect(url_for("signup"))


# -------------------------
# Signup Page
# -------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        conn = get_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            conn.close()
            return "Email already exists!"

        # Insert new user
        sql = """
        INSERT INTO users(name, email, password, phone)
        VALUES (%s, %s, %s, %s)
        """

        values = (name, email, password, phone)

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


# -------------------------
# Login Page
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """

        cursor.execute(sql, (email, password))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return render_template("dashboard.html", user=user)

        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# -------------------------
# Dashboard
# -------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -------------------------
# Run Flask
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)