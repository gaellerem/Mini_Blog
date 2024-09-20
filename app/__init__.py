from flask import Flask, render_template
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFError
from config import Config
from app.extensions import db, login_manager, csrf, admin
from app.models import User, Post
from app.admin_views import IndexView, UserAdmin, PostAdmin

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate=Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page"
    login_manager.login_message_category = "warning"
    csrf.init_app(app)
    admin.init_app(app, index_view=IndexView())
    admin.add_view(UserAdmin(User, db.session, name="Utilisateurs"))
    admin.add_view(PostAdmin(Post, db.session, name="Articles"))

    from app.posts import bp as post_bp
    app.register_blueprint(post_bp, url_prefix='/post')

    from app.users import bp as user_bp
    app.register_blueprint(user_bp)

    @app.route('/')
    def index():
        posts = Post.query.order_by(Post.created.desc()).all()
        return render_template('index.html', posts=posts)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/csrf_error.html', reason="Le jeton CSRF est manquant"), 403

    return app

from app.models import load_user