from flask import Blueprint, request, redirect, url_for, render_template, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Minimal stub: show login form on GET; accept POST and redirect to home for local testing.
    if request.method == 'POST':
        # In a real app you'd validate credentials and create a session.
        email = request.form.get('email')
        remember = request.form.get('remember')
        # For debugging, you can print or log email/remember
    # After a successful (stub) login redirect to the main.home endpoint
    return redirect(url_for('main.home'))

    # GET -> show the login page
    return render_template('login.html')


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # TODO: verify email exists and send reset link
        flash("If this email is registered, a password reset link was sent.")
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')
