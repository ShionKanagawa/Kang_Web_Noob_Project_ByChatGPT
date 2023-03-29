from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from markdown.inlinepatterns import InlineProcessor



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'



def _highlight_code(self, code, lang):
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)
    

    
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

# 将 Markdown 转换为 HTML

def md(text):
    # Create a Markdown renderer object
    renderer = markdown.Markdown()

    # Define a function to handle code highlighting
    def highlight_code(text):
        # custom code highlighting logic here
        return highlighted_text

    # Replace the handleMatch method of InlineCodeProcessor with the highlight_code function
    InlineProcessor.handleMatch = highlight_code

    # Render the Markdown text using the modified renderer object
    html = renderer.convert(text)
    return html


app.jinja_env.filters['md'] = md
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
