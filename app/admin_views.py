from flask import redirect, url_for, request, flash
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField
from wtforms.validators import EqualTo
from app.models import User, Post
from app.webforms import CreateUserForm


class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.is_admin):
            return redirect(url_for('users.login', next=request.url))

        admin_count = User.query.filter_by(is_admin=True).count()
        user_count = User.query.count()
        post_count = Post.query.count()
        recent_users = User.query.order_by(User.created.desc()).limit(5).all()
        recent_posts = Post.query.order_by(Post.created.desc()).limit(5).all()

        return self.render('admin/index.html', admin_count=admin_count, user_count=user_count, post_count=post_count, recent_users=recent_users, recent_posts=recent_posts)

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
    column_formatters = { 
        'created': lambda v, c, m, p: m.created.strftime("%d-%m-%Y"),
        'posts': lambda v, c, m, p: len(m.posts)
    }
    column_labels = {
        'id': 'ID', 
        'username': 'Pseudo', 
        'email': 'Adresse mail',
        'created': "Membre depuis",
        'posts': "Articles",
        "is_admin": "Est admin",
    }
    column_list = ('id', 'username', 'email', 'created', 'posts', 'is_admin')
    column_sortable_list = ('id', 'username', 'email', 'created', 'posts', 'is_admin')

    form_excluded_columns = ('password_hash', 'posts')
    form_extra_fields = {  # Ajout d'un input password et confirm pour crypter à la validation
        'password': PasswordField(
            'Nouveau mot de passe',
            validators=[EqualTo('confirm', message="Les mots de passe doivent correspondre")]),
        'confirm': PasswordField('Confirmer le nouveau mot de passe')
    }

    can_view_details = True

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

    @expose('/<int:id>')
    def details_view(self, id):
        user = User.query.get_or_404(id)
        return_url = self.get_url('.index_view')
        return self.render('admin/details_user.html', user=user, return_url=return_url)


class PostAdmin(AdminModelView):
    column_formatters = {
        'created': lambda v, c, m, p: m.created.strftime("%d-%m-%Y %H:%M"),
        'user': lambda v, c, m, p: User.query.get(m.user_id).username
    }
    column_labels = {'user': 'Auteurice',
                     'title': 'Titre', 'created': "Mise en ligne", "content": "Contenu"}

    column_list = ('user', 'title', 'created')
    
    can_view_details = True
    column_details_list = ('user', 'created', 'title', 'content')

