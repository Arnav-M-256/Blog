from logging import makeLogRecord
import flask
from flask import render_template, request, make_response
import sqlite3
from werkzeug.exceptions import abort

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

def user_exists(email):
    conn = get_db_connection()
    record = conn.execute(f"SELECT * FROM credentials WHERE email = '{email}'").fetchall()
    conn.close()
    return len(record) == 1

app = flask.Flask(__name__)

@app.route('/')
def index():
    books = get_all_books()
    return render_template('index.html', books=books)


@app.route('/<int:book_id>')
def book_details(book_id):
    book = get_book(book_id)
    return render_template('book.html', book=book)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    user = conn.execute(f"SELECT * FROM credentials WHERE email = '{email}' AND password = '{password}'").fetchall()
    conn.close()
    if len(user) != 1:
        abort(401)

    resp = make_response(render_template('index.html', books=posts))
    resp.set_cookie(key='email', value=f'{email}', max_age=3600) # max_age in seconds so 1 hour
    return resp

@app.route('/make_account')
def make_account():
    return render_template('new_user.html')


@app.route('/new_user', methods=['POST'] )
def new_user():
    email = request.form['email']
    password = request.form['password']

    if user_exists(email):
        return login()
    
    conn = get_db_connection()
    conn.execute(f"INSERT INTO credentials (email, password) VALUES ('{email}', '{password}')")
    conn.commit()
    conn.close()
    return login()


@app.route('/get_user')
def get_user():
    email = request.cookies.get('email')
    if not email:
        return '<h1>Please Log In!</h1>'
    return '<h1>Welcome ' + email + '</h1>'

@app.route('/logout')
def logout():
    resp = make_response(index())
    flask.Response.delete_cookie(resp, key='email')
    return resp