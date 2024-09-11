from flask import redirect, url_for, request, flash
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField
from wtforms.validators import EqualTo
from wtforms_alchemy.fields import QuerySelectField
from app.models import User, Post
from app.webforms import CreateUserForm


class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.is_admin):
            return redirect(url_for('users.login', next=request.url))

        user_count = User.query.count()
        post_count = Post.query.count()
        recent_users = User.query.order_by(User.created.desc()).limit(5).all()
        recent_posts = Post.query.order_by(Post.created.desc()).limit(5).all()

        return self.render('admin/index.html', user_count=user_count, post_count=post_count, recent_users=recent_users, recent_posts=recent_posts)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login', next=request.url))


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login'))


class UserAdmin(AdminModelView):
    def _format_created(view, context, model, name):
        return model.created.strftime("%d-%m-%Y %H:%M")

    column_list = ('id', 'username', 'email', 'created', 'is_admin')
    column_labels = {'id': 'ID', 'username': 'Pseudo', 'email': 'Adresse mail',
                     'created': "Membre depuis", "is_admin": "Est admin"}
    # exlure le mot de passe crypté
    form_excluded_columns = ('password_hash')
    # Ajout d'un input password et confirm pour crypter à la validation
    form_extra_fields = {
        'password': PasswordField(
            'Nouveau mot de passe',
            validators=[EqualTo('confirm', message="Les mots de passe doivent correspondre")]),
        'confirm': PasswordField('Confirmer le nouveau mot de passe')
    }

    column_formatters = {
        'created': _format_created
    }

    def create_form(self, obj=None):
        return CreateUserForm()

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = form.password.data
        return super(UserAdmin, self).on_model_change(form, model, is_created)

    def delete_model(self, model):
        if model.is_admin:
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count <= 1:
                flash("Impossible de supprimer le dernier administrateur.", "error")
                return False
        return super(UserAdmin, self).delete_model(model)


class PostAdmin(AdminModelView):
    column_list = ('user_id', 'title', 'content')
    column_labels = {'user_id': 'ID Auteurice',
                     'title': 'Titre', 'content': 'Contenu'}
    form_extra_fields = {
        'user': QuerySelectField('Auteurice', query_factory=lambda: User.query, get_label='username')
    }

    def on_model_change(self, form, model, is_created):
        model.user_id = form.user.data.id
        return super(PostAdmin, self).on_model_change(form, model, is_created)
