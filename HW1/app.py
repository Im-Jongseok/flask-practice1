from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "home.html",
        name="이종석",
        student_id="21011615",
    )
