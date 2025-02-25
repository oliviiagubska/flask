from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    username = request.args.get("username")
    password = request.args.get("password")
    if username == None:
        return render_template("index.html")
    elif password == "123":
        return "Hello" + username
    else:
        return "wrong password"
