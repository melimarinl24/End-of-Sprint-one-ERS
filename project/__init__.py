from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import logging      
import os
from dotenv import load_dotenv

db=SQLAlchemy()
login_manager=LoginManager()

def create_app():
    app=Flask(__name__)

    load_dotenv()

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

    # Register routes from views.py
    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    return app
