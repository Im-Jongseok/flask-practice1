from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(200))
    done = db.Column(db.Boolean, default=False)

    def __init__(self, text, note=''):
        self.text = text
        self.note = note
        self.done = False

    def __repr__(self):
        return f'<Todo {self.id}: {self.text}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('todo', '').strip()
        note = request.form.get('note', '')
        if not 1 <= len(text) <= 100 or len(note) > 200:
            return '할 일은 1~100자, 설명은 200자 이하로 입력해주세요.', 400
        todo = Todo(text=text, note=note)

        db.session.add(todo)
        db.session.commit()

        return redirect(url_for('index'))

    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = db.get_or_404(Todo, id)
    if request.method == 'POST':
        text = request.form.get('todo', '').strip()
        note = request.form.get('note', '')
        if not 1 <= len(text) <= 100 or len(note) > 200:
            return '할 일은 1~100자, 설명은 200자 이하로 입력해주세요.', 400
        todo.text = text
        todo.note = note
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)


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


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
