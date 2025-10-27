from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user
import re

auth = Blueprint('auth', __name__)

NSHE_RE = re.compile(r'^\d{10}$')
FACULTY_EMAIL_RE = re.compile(r'^[A-Za-z]+(?:\.[A-Za-z]+)*@csn\.edu$')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print("HIT /signup", request.method, request.path)

    roles = ['Student', 'Faculty']  # for template dropdown if you use it

    if request.method == 'GET':
        return render_template('signup.html', roles=roles)

    # ---------- POST ----------
    # Normalize role to lower for logic, keep Title for messages
    raw_role   = (request.form.get('role') or '').strip()
    role_lower = raw_role.lower()
    role_title = 'Student' if role_lower == 'student' else 'Faculty' if role_lower == 'faculty' else raw_role.title()

    first_name = (request.form.get('first_name') or '').strip()
    last_name  = (request.form.get('last_name') or '').strip()
    phone      = (request.form.get('phone') or '').strip()

    # Student-only
    nshe       = (request.form.get('nshe') or '').strip()
    major      = (request.form.get('major') or '').strip()

    # Faculty-only
    department = (request.form.get('department') or '').strip()
    employee_id= (request.form.get('employee_id') or '').strip()

    # --- basic checks (no email here; it's role-specific) ---
    if role_lower not in ('student', 'faculty'):
        return render_template('signup.html', roles=roles, errorMsg='Please choose Student or Faculty.')

    if not first_name or not last_name or not phone:
        return render_template('signup.html', roles=roles, errorMsg='First name, last name, and phone are required.')

    # --- role-specific validation ---
    if role_lower == 'student':
        email = (request.form.get('email') or '').strip().lower()
        if not NSHE_RE.match(nshe):
            return render_template('signup.html', roles=roles, errorMsg='NSHE must be exactly 10 digits.')
        if not email.endswith('@student.csn.edu'):
            return render_template('signup.html', roles=roles, errorMsg='Student email must end with @student.csn.edu.')
        if not major:
            return render_template('signup.html', roles=roles, errorMsg='Please choose your major.')
        # TODO: create student in DB here

    elif role_lower == 'faculty':
        email = (request.form.get('email') or '').strip().lower()
        if not FACULTY_EMAIL_RE.match(email):
            return render_template('signup.html', roles=roles, errorMsg='Faculty email must be firstname.lastname@csn.edu.')
        if not department:
            return render_template('signup.html', roles=roles, errorMsg='Department is required.')
        if not employee_id:
            return render_template('signup.html', roles=roles, errorMsg='Employee ID is required.')
        # TODO: create faculty in DB here

    # Success → go to login
    flash(f'{role_title} account created (stub). Please log in.', 'success')
    return redirect(url_for('auth.login'))


# auth.py
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        remember = bool(request.form.get('remember'))

        # TODO: authenticate against DB
        flash('Logged in (stub).', 'success')
        # send them wherever you want after login:
        return redirect(url_for('main.dashboard'))  # or a dashboard route
    return render_template('login.html')



@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return render_template('logout.html')



@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # TODO: verify email exists and send reset link
        flash("If this email is registered, a password reset link was sent.")
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')
