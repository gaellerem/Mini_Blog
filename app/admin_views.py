from flask import redirect, url_for, request, flash
from flask_admin import AdminIndexView, expose
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.models import User, Post

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
    column_list = ('id', 'username', 'email', 'created', 'is_admin')
    column_labels = {'id': 'ID', 'username': 'Username', 'email': 'Email Address', 'created' : "Membre depuis", "is_admin": "Is Admin"}
    form_excluded_columns = ('password_hash')
    can_create = False

    def _format_created(view, context, model, name):
        return model.created.strftime("%d-%m-%Y %H:%M")

    column_formatters = {
        'created': _format_created
    }

    def delete_model(self, model):
        if model.is_admin:
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count <= 1:
                flash("Impossible de supprimer le dernier administrateur.", "error")
                return False
        return super(UserAdmin, self).delete_model(model)

class PostAdmin(AdminModelView):
    column_list = ('title', 'user_id', 'content')
    column_labels = {'title': 'Post Title', 'user_id': 'Author ID', 'content': 'Content'}