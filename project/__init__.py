from flask import Flask, app, request, jsonify, redirect, url_for, render_template
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

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-only-change-me")

    app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
    app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}"
        f"@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}"
    )
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = "strong"
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    

    # Import models so create_all sees them (add your models here)
    with app.app_context():
        # from .exams import Exam  # if you have this model
        # from .models import User # when you add it
        db.create_all()

    # Register blueprints here

    from .views import bp as main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    from .student_ui import student_ui
    app.register_blueprint(student_ui)

    from .faculty_ui import faculty_ui
    app.register_blueprint(faculty_ui)

    return app
