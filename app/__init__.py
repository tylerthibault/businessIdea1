from flask import Flask, render_template
from .config import config_map
from .extensions import db, login_manager, migrate

def create_app(env='development'):
    app = Flask(__name__)
    app.config.from_object(config_map[env])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    from .models.user import User
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))

    from .controllers import landing, auth, dashboard, clients, quotes, public
    app.register_blueprint(landing.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(quotes.bp)
    app.register_blueprint(public.bp)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app
