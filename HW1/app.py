from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "home.html",
        name="이종석",
        student_id="21011615",
    )


@app.route("/profile")
def profile():
    hobbies = ["독서", "자전거", "등산"]
    return render_template(
        "profile.html",
        name="이종석",
        hobbies=hobbies,
    )


@app.route("/greet/<name>")
def greet(name):
    return render_template("greet.html", name=name)
