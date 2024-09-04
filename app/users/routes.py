from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from app.users import bp
from app.extensions import db
from app.models.user import User
from app.webforms import SignUpForm, LogInForm, EditUserForm

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('users.html', users=users)


@bp.route('/signup', methods=('GET', 'POST'))
def add_user():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():
        user_by_email = User.query.filter_by(email=form.email.data).first()
        user_by_username = User.query.filter_by(username=form.username.data).first()
        if user_by_email:
            flash('Email déjà utilisé.', 'warning')
        elif user_by_username:
            flash('Nom d\'utilisateur déjà utilisé.', 'warning')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                role='user'
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('users.dashboard'))
    return render_template('signup.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Mot de passe incorrect", 'danger')
        else:
            flash("Identifiant inconnu", "danger")
    return render_template('login.html', form=form)


@bp.route('/logout', methods=('GET', 'POST'))
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/user/edit', methods=('GET', 'POST'))
@login_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        current_user.username = username
        current_user.email = email
        db.session.commit()
        return redirect(url_for('users.dashboard'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('edit_user.html', form=form)


@bp.route('/user/delete', methods=['POST'])
@login_required
def delete_user():
    user = User.query.get_or_404(current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash('Profile was successfully deleted!', 'success')
    return redirect(url_for('users.index'))


@bp.route('/dashboard')
@login_required
def dashboard():
    posts = current_user.posts
    return render_template('dashboard.html', posts=posts)