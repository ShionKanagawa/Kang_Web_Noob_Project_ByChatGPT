from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from markdown import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.add_template_filter(markdown, 'markdown')



# 创建数据库表
def create_table():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  message TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# 插入留言到数据库
def insert_message(name, message):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    message=markdown(message)
    c.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (name, message))
    conn.commit()
    conn.close()

# 获取所有留言
def get_messages():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages ORDER BY id DESC')
    messages = c.fetchall()
    conn.close()
    return messages

@app.route('/')
def index():
    messages = get_messages()
    return render_template('index.html.jinja2', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']
    insert_message(name, message)
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)