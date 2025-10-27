from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import logging      
import os
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():  
    app=Flask(__name__)

    load_dotenv()

    # Prefer an env var; fall back to a dev key so your app runs locally.
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-change-me')

    # Ensure basic logging is configured if the host didn't set it
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

    # During local development, allow templates to auto-reload when changed.
    # This is safe because the app is bound to 127.0.0.1 by default in run.py.
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Load DB credentials from environment (set these in a local .env file or via OS env vars)
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_db = os.getenv("MYSQL_DB")

    if not all([mysql_host, mysql_user, mysql_password, mysql_db]):
        logging.getLogger(__name__).warning(
            "One or more MYSQL_* environment variables are not set. "
            "SQLALCHEMY_DATABASE_URI will not be configured until they are provided."
        )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
        )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 6) Make current_user safe in Jinja even before auth is fully wired
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # Register routes from views.py
    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from .student_ui import student_ui
    app.register_blueprint(student_ui)


    # Flask-Login user loader (lazy import to avoid ModuleNotFoundError if models.py not ready)
    @login_manager.user_loader
    def load_user(user_id):
        try:
            from .models import User  # imported only when needed
            return User.query.get(int(user_id))
        except Exception:
            return None
    # DEBUG: list routes once at startup
    for rule in app.url_map.iter_rules():
        if '/signup' in str(rule):
            print('ROUTE:', rule.rule, '-> endpoint:', rule.endpoint, 'methods:', sorted(rule.methods))

    return app