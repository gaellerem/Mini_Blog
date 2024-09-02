from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_post_with_username(post_id):
    conn = get_db_connection()
    try:
        post = conn.execute('''
            SELECT posts.title, posts.content, posts.created, users.username 
            FROM posts 
            INNER JOIN users ON users.id = posts.userId 
            WHERE posts.id = ?
        ''', (post_id,)).fetchone()
    finally:
        conn.close()

    if post is None:
        abort(404)

    return post


app = Flask(__name__)
app.config["SECRET_KEY"] = 'cgLN0zPgBqcN1xNjnKfma7oM2ZLkPd5D'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/user/<string:name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = get_post_with_username(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now()
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, created, userId) VALUES (?, ?, ?, ?)',
                         (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/post/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/post/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500