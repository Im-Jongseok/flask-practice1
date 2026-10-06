from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return f"<a href='/about'>소개로</a>"

@app.route("/info")
def about_page():
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

@app.route("/search")
def search():
    query = request.args.get("q", '')
    page = request.args.get("page", '1')
    if not query:
        return "<h1>검색어를 입력해주세요.</h1>"
    return f"<h1>'{query}' 검색 결과 {page} 페이지</h1>"

@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "POST":
        banana = request.form["banana"]
        melon = request.form["melon"]
        return (f'banana = {banana} ({type(banana).__name__}) / '
                f'melon = {melon} ({type(melon).__name__})')
    return '''
    <form method="post">
        <input type="text" name="banana">
        <input type="text" name="melon" >
        <button type="submit">보내기</button>
    </form>'''

@app.route("/attach", methods=["GET", "POST"])
def attach():
    if request.method == "POST":
        file = request.files.get("cherry")
        if file is None:
            return 'cherry가 files에 없습니다.'
        return f'{file.filename} / {len(file.read())} bytes.'
    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="cherry">
        <button type="submit">보내기</button>
    </form>'''