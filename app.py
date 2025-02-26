from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        f = open("login.txt", "w")
        f.write(username + "\n")
        f.write(password)
        f.close()
        return "Sign up success"

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        f = open("login.txt", "r")
        username = f.readline().strip()
        password = f.readline()
        if username == request.form["username"] and \
           password == request.form["password"]:
           return "Hello " + username
        else:
            return "login failed"