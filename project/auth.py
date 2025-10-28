# project/auth.py
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

from . import db
from .models import User, Role, Department, Major  # adjust if your models are in a different file

auth = Blueprint('auth', __name__)

# strict patterns
NSHE_RE = re.compile(r'^\d{10}$')
STUDENT_EMAIL_RE = re.compile(r'^(\d{10})@student\.csn\.edu$', re.I)
FACULTY_EMAIL_RE = re.compile(r'^[A-Za-z]+(?:\.[A-Za-z]+)*@csn\.edu$', re.I)

def _email_lower(s: str) -> str:
    return (s or '').strip().lower()

def _clean(s: str) -> str:
    return (s or '').strip()

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    roles = ['Student', 'Faculty']

    # ---------- GET ----------
    if request.method == 'GET':
        departments = Department.query.all()
        return render_template('signup.html', roles=roles, departments=departments)

    # ---------- POST ----------
    departments = Department.query.all()  # always available on POST too

    role_raw   = _clean(request.form.get('role'))
    role_lower = role_raw.lower()
    first_name = _clean(request.form.get('first_name'))
    last_name  = _clean(request.form.get('last_name'))
    phone      = _clean(request.form.get('phone'))
    email      = _email_lower(request.form.get('email'))

    if role_lower not in ('student', 'faculty'):
        return render_template('signup.html', roles=roles, departments=departments,
                               errorMsg='Please choose Student or Faculty.')

    if not first_name or not last_name or not phone:
        return render_template('signup.html', roles=roles, departments=departments,
                               errorMsg='First name, last name, and phone are required.')

    nshe        = _clean(request.form.get('nshe'))
    major_name  = _clean(request.form.get('major'))
    department_id = request.form.get('department_id')  # <-- IMPORTANT: now uses FK
    employee_id = _clean(request.form.get('employee_id'))

    # Validate student vs faculty
    password_plain = None

    if role_lower == 'student':
        m = STUDENT_EMAIL_RE.match(email)
        if not m:
            return render_template('signup.html', roles=roles, departments=departments,
                                   errorMsg='Student email must be NSHEID@student.csn.edu.')
        email_nshe = m.group(1)

        if not NSHE_RE.match(nshe):
            return render_template('signup.html', roles=roles, departments=departments,
                                   errorMsg='NSHE must be 10 digits.')
        if nshe != email_nshe:
            return render_template('signup.html', roles=roles, departments=departments,
                                   errorMsg='NSHE must match the email NSHE (before @).')

        if not major_name:
            return render_template('signup.html', roles=roles, departments=departments,
                                   errorMsg='Please choose your major.')

        password_plain = nshe

    else:  # faculty
        if not FACULTY_EMAIL_RE.match(email):
            return render_template('signup.html', roles=roles, departments=departments,
                                   errorMsg='Faculty email must be firstname.lastname@csn.edu.')

        if not department_id:
            return render_template('signup.html', roles=roles, departments=departments,
                                   errorMsg='Department is required.')

        if not employee_id:
            return render_template('signup.html', roles=roles, departments=departments,
                                   errorMsg='Employee ID is required.')

        password_plain = employee_id

    # Duplicate protection
    if User.query.filter_by(email=email).first():
        return render_template('signup.html', roles=roles, departments=departments,
                               errorMsg='This email is already registered.')
    if role_lower == 'student' and User.query.filter_by(nshe_id=nshe).first():
        return render_template('signup.html', roles=roles, departments=departments,
                               errorMsg='This NSHE is already registered.')

    # FK resolution
    role = Role.query.filter_by(name=role_lower.title()).first()
    major = Major.query.filter_by(name=major_name).first() if role_lower == 'student' else None
    dept = Department.query.get(department_id) if role_lower == 'faculty' else None

    # Create user
    full_name = f'{first_name} {last_name}'.strip()
    password_hash = generate_password_hash(password_plain)

    user = User(
        name=full_name,
        email=email,
        phone=phone,
        nshe_id=nshe if role_lower == 'student' else None,
        employee_id=employee_id if role_lower == 'faculty' else None,
        role_id=getattr(role, 'id', None),
        major_id=getattr(major, 'id', None),
        department_id=getattr(dept, 'id', None),
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    login_user(user, remember=True)

    # redirect to role dashboard
    if role_lower == 'student':
        return redirect(url_for('student_ui.student_dashboard'))
    return redirect(url_for('faculty_ui.faculty_dashboard'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = _email_lower(request.form.get('email'))
        password = request.form.get('password') or ''
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(email=email).first()
        if not user or not user.password_hash or not check_password_hash(user.password_hash, password):
            return render_template('login.html', errorMsg='Invalid email or password.')

        login_user(user, remember=remember)

        if getattr(getattr(user, 'role', None), 'name', '').lower() == 'faculty' or user.employee_id:
            return redirect(url_for('faculty_ui.faculty_dashboard'))
        return redirect(url_for('student_ui.student_dashboard'))

    return render_template('login.html')

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        flash("If this email is registered, a reset link was sent.")
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')
