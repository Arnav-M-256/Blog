import flask
from flask import render_template
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute(f'SELECT * FROM books WHERE bookID = {book_id}').fetchone()
    conn.close()
    return book

def get_all_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return books

app = flask.Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

