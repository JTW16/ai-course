import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(BASE_DIR, 'schema.sql')


def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    conn = connect(db_path)
    with open(SCHEMA, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def get_todos(db_path):
    conn = connect(db_path)
    # 생성 시각 내림차순 정렬 (같은 초에 생성된 항목은 나중에 추가된 것이 위로)
    todos = conn.execute('SELECT * FROM todos ORDER BY created_at DESC, id DESC').fetchall()
    conn.close()
    return todos


def add_todo(db_path, title):
    conn = connect(db_path)
    conn.execute('INSERT INTO todos (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()


def toggle_todo(db_path, todo_id):
    """완료 상태를 반전한다. 해당 ID가 없으면 False를 반환한다."""
    conn = connect(db_path)
    todo = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    if todo is None:
        conn.close()
        return False

    new_status = 0 if todo['is_completed'] else 1
    conn.execute('UPDATE todos SET is_completed = ? WHERE id = ?', (new_status, todo_id))
    conn.commit()
    conn.close()
    return True


def delete_todo(db_path, todo_id):
    """할 일을 삭제한다. 해당 ID가 없으면 False를 반환한다."""
    conn = connect(db_path)
    cur = conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0
