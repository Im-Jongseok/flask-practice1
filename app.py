from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return f"<a href='{url_for('about')}'>소개로</a>"


@app.route("/about")
def about():
    return "<h1>소개 페이지</h1>"

@app.route("/user/<username>")
def profile(username):
    return f"<h1>{username}님의 프로필</h1>"

@app.route("/post/<int:pid>")
def post(pid):
    return f"<h1>{pid}번 글 (자료형: {type(pid).__name__})</h1>"

@app.route("/notes/")
def notes():
    return "<h1>메모 목록</h1>"

@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    if name:
        return f"<h1>안녕하세요, {name}!</h1>"
    return "<h1>안녕하세요!</h1>"