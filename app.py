import bcrypt
from datetime import datetime
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import os
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, InputRequired, EqualTo

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
app.config["SECRET_KEY"] = 'cgLN0zPgBqcN1xNjnKfma7oM2ZLkPd5D'
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<User "{self.username}">'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post "{self.title}">'

class SignUpForm(FlaskForm):
    username = StringField("Votre pseudo", validators=[InputRequired()])
    email = StringField("Votre email", validators=[Email()])
    password = PasswordField('Votre mot de passe', validators=[InputRequired()])
    submit = SubmitField("Créer votre compte")


class SignInForm(FlaskForm):
    username = StringField("Votre pseudo", validators=[InputRequired()])
    password = PasswordField('Votre mot de passe', validators=[InputRequired()])
    submit = SubmitField("Créer votre compte")


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>/delete', methods=('POST',))
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User was successfully deleted!', 'success')
    return redirect(url_for('users'))

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            user = User(
                username=form.username.data, 
                email=form.email.data,
                password=password,
                role='user'
            )
            db.session.add(user)
            db.session.commit()
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''
        return redirect(url_for('users'))
    return render_template('signup.html', form=form)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/post/create', methods=('GET', 'POST'))
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            post = Post(title=title, content=content, user_id=1)  # Remplacez 1 par l'ID de l'utilisateur actuel
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/post/<int:post_id>/edit', methods=('GET', 'POST'))
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            post.title = title
            post.content = content
            db.session.commit()
            return redirect(url_for('post', post_id=post.id))

    return render_template('edit.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=('POST',))
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post was successfully deleted!', 'success')
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