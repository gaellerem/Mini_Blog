from flask import Flask, render_template
from flask_migrate import Migrate
from config import Config
from app.extensions import db, login_manager
from app.models.post import Post


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate=Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = "Veuillez vous connecter"
    login_manager.login_message_category = "warning"

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    @app.route('/')
    def index():
        posts = Post.query.order_by(Post.created.desc()).all()
        return render_template('index.html', posts=posts)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html'), 500

    return app
