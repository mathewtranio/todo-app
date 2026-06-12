from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("todo.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    todos = conn.execute('SELECT * FROM todos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title', '').strip()
    if title:
        conn = get_db()
        conn.execute('INSERT INTO todos (title) VALUES (?)', (title,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete_todo(id):
    conn = get_db()
    todo = conn.execute('SELECT * FROM todos WHERE id=?', (id,)).fetchone()
    new_status = 0 if todo['completed'] else 1
    conn.execute('UPDATE todos SET completed=? WHERE id=?', (new_status, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_todo(id):
    conn = get_db()
    conn.execute('DELETE FROM todos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
