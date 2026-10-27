import os

from flask import Blueprint, Flask, redirect, render_template, request, url_for
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'TODO_DATABASE_URI', 'sqlite:///todos.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["ERROR_404_HELP"] = False
app.config["RESTX_JSON"] = {"ensure_ascii": False}

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    note = db.Column(db.String(500), default="")

    def __init__(self, text, done=False, note=""):
        self.text = text
        self.done = done
        self.note = note

    def __repr__(self):
        return f'<Todo {self.id}: {self.text}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['todo']
        todo = Todo(text=text)

        db.session.add(todo)
        db.session.commit()

        return redirect(url_for('index'))

    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/delete/<int:id>')
def delete(id):
    todo = db.get_or_404(Todo, id)
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/toggle/<int:id>')
def toggle(id):
    todo = db.get_or_404(Todo, id)
    todo.done = not todo.done
    db.session.commit()

    return redirect(url_for('index'))


api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(
    api_bp,
    version="1.0",
    title="Todo API",
    description="[4장] todo 앱 API",
    doc="/docs",
)
ns = api.namespace("todos", description="할 일 관리")

# 주고받을 데이터의 모양입니다. 이것이 곧 문서가 됩니다.
todo_model = api.model("Todo", {
    "id": fields.Integer(readonly=True, description="줄 번호. 서버가 붙입니다"),
    "text": fields.String(required=True, description="할 일 글자", example="우유 사기"),
    "done": fields.Boolean(description="완료 여부", example=False),
    "note": fields.String(description="설명", example="2리터짜리로"),
})
# 만들 때와 바꿀 때 받을 것. id 는 받지 않습니다.
todo_input = api.model("TodoInput", {
    "text": fields.String(required=True, description="할 일 글자", example="우유 사기"),
    "done": fields.Boolean(description="완료 여부", example=False),
    "note": fields.String(description="설명", example="2리터짜리로"),
})


@ns.route("/")
class TodoList(Resource):
    @ns.doc("목록 보기")
    @ns.param("done", "true면 완료만, false면 미완료만 조회")
    @ns.marshal_list_with(todo_model)
    def get(self):
        """할 일 목록을 조회하고 done이 있으면 완료 여부로 필터링한다"""
        query = Todo.query
        done = request.args.get("done")
        if done is not None:
            query = query.filter_by(done=(done.lower() == "true"))
        return query.all()

    @ns.doc("새로 만들기")
    @ns.expect(todo_input, validate=True)
    @ns.marshal_with(todo_model, code=201)  # pyright: ignore[reportArgumentType]
    def post(self):
        """할 일을 하나 만든다"""
        todo = Todo(
            text=api.payload["text"],
            done=api.payload.get("done", False),
            note=api.payload.get("note", ""),
        )
        db.session.add(todo)
        db.session.commit()
        # 만들었으면 201 과 함께 그것이 어디 있는지 Location 에 적어 줍니다.
        return todo, 201, {"Location": f"/api/todos/{todo.id}"}


@ns.route("/<int:id>")
@ns.param("id", "할 일의 줄 번호")
@ns.response(404, "그 번호의 할 일이 없습니다")
class TodoItem(Resource):
    @ns.doc("하나 보기")
    @ns.marshal_with(todo_model)
    def get(self, id):
        """할 일 하나를 돌려준다"""
        return get_or_abort(id)

    @ns.doc("통째로 바꾸기")
    @ns.expect(todo_input, validate=True)
    @ns.marshal_with(todo_model)
    def put(self, id):
        """할 일 하나를 통째로 바꾼다. 보내지 않은 칸은 기본값이 된다"""
        todo = get_or_abort(id)
        todo.text = api.payload["text"]
        todo.done = api.payload.get("done", False)
        todo.note = api.payload.get("note", "")
        db.session.commit()
        return todo

    @ns.doc("일부만 바꾸기")
    @ns.expect(todo_input)
    @ns.marshal_with(todo_model)
    def patch(self, id):
        """보낸 칸만 바꾼다. 완료 표시를 뒤집을 때 씁니다"""
        todo = get_or_abort(id)
        if "text" in api.payload:
            todo.text = api.payload["text"]
        if "done" in api.payload:
            todo.done = api.payload["done"]
        if "note" in api.payload:
            todo.note = api.payload["note"]
        db.session.commit()
        return todo

    @ns.doc("지우기")
    @ns.response(204, "지웠습니다. 돌려줄 내용이 없습니다")
    def delete(self, id):
        """할 일 하나를 지운다"""
        todo = get_or_abort(id)
        db.session.delete(todo)
        db.session.commit()
        return "", 204


def get_or_abort(id: int) -> Todo:
    return db.get_or_404(
        Todo,
        id,
        description=f"{id} 번 할 일이 없습니다",
    )


app.register_blueprint(api_bp)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
