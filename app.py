from flask import Flask, render_template, request, session, redirect
import sqlite3
import hashlib
app = Flask(__name__)
app.secret_key = 'random'


con = sqlite3.connect("login.db")
cur = con.cursor()
cur.execute(''' CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(10) NOT NULL PRIMARY KEY,
                password VARCHAR(20) NOT NULL
            )''')
con.commit()
con.close()

@app.route("/")
def start():
    return render_template("home.html")

import re
from flask import Flask, render_template, request, session, redirect

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        # ccheck password strength
        if len(password) < 6 or not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            return render_template("signup.html", error="Password must be at least 6 characters and include both letters and numbers.")

        #Check if username exists
        con = sqlite3.connect("login.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing = cur.fetchone()
        if existing:
            con.close()
            return render_template("signup.html", error="Username already taken. Please choose another.")

        
        hash = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash))
        con.commit()
        con.close()

        return redirect("/login")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        con = sqlite3.connect("login.db")
        cur = con.cursor()
        hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                    (request.form["username"], hash))
        user = cur.fetchone()
        print(user)
        if user:
            session["username"] = request.form["username"]
            return render_template("welcome.html")
        else:
            return render_template("login_failed.html")

@app.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "GET":
        if "username" in session:
            return render_template("password.html")
        else:
            return render_template("index.html")
    else:
        con = sqlite3.connect("login.db")
        cur = con.cursor()
        hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
        cur.execute(""" UPDATE users SET password=? WHERE username=?""",
                    (hash, session["username"]))
        con.commit()
        con.close()
        return render_template("password_success.html")
    
@app.route("/w")
def welcome():
    return render_template("welcome.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template("index.html")

@app.route("/create_team", methods=["GET", "POST"])
def create_team():
    if request.method == "POST":
        team_name = request.form["team_name"]
        invites_raw = request.form["invites"]

        invites = [email.strip() for email in invites_raw.splitlines() if email.strip()]
        owner = session["username"]

        con = sqlite3.connect("login.db")
        cur = con.cursor()

        #Insert new team
        cur.execute("INSERT INTO teams (name, owner) VALUES (?, ?)", (team_name, owner))
        team_id = cur.lastrowid  #get the ID of the new team

        #Insert invited members
        for email in invites:
            cur.execute("INSERT INTO team_members (team_id, email) VALUES (?, ?)", (team_id, email))

        con.commit()
        con.close()

        return redirect("/w") 

    return render_template("create_team.html")


@app.route("/join_team")
def join_team():
    return render_template("join_team.html")

if __name__ == "__main__":
    app.run(debug=True)