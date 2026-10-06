import os
from flask import Flask, render_template, request, redirect, url_for, abort

import db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
DATABASE = os.path.join(BASE_DIR, 'database.db')


# DATABASE는 호출 시점에 읽는다 (테스트가 경로를 바꿀 수 있도록)
def init_db():
    db.init_db(DATABASE)


@app.route('/')
def index():
    all_todos = db.get_todos(DATABASE)
    incomplete_todos = [t for t in all_todos if not t['is_completed']]
    completed_todos = [t for t in all_todos if t['is_completed']]
    return render_template('index.html', incomplete_todos=incomplete_todos, completed_todos=completed_todos)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if not title:
        abort(400)

    db.add_todo(DATABASE, title)
    return redirect(url_for('index'))


@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    if not db.toggle_todo(DATABASE, todo_id):
        abort(404)
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    if not db.delete_todo(DATABASE, todo_id):
        abort(404)
    return redirect(url_for('index'))


# `flask run`으로 실행해도 테이블이 준비되도록 import 시점에 초기화
init_db()

if __name__ == '__main__':
    app.run(debug=True)
