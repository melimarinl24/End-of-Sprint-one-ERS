from flask import Blueprint, render_template, jsonify, current_app, redirect, url_for, request, flash
from . import db
from sqlalchemy import text
import os
import time
import logging

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'], endpoint='home')
def home():
    # Serve the hero homepage at the site root so the header Home link
    # points to the intended landing page rather than the login view.
    try:
        return render_template('home.html')
    except Exception:
        # Fall back to the login template if the home template is missing
        return render_template('index.html')


@bp.route('/Sign up', methods=['GET'])
def Signup():
    return jsonify({'message': 'Sign up'})


@bp.route('/signup/student', methods=['GET', 'POST'], endpoint='signup_student')
def signup_student():
    """Simple student signup/info page that directs users to the login flow."""
    try:
        if request.method == 'POST':
            first = request.form.get('first_name', '').strip()
            last = request.form.get('last_name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            nshe = request.form.get('nshe', '').strip()
            major = request.form.get('major', '').strip()

            # Basic validation
            if not email:
                return render_template('signup_student.html', errorMsg="Please provide an email address")

            if not email.endswith("@student.csn.edu"):
                return render_template('signup_student.html', errorMsg="Email must end with @student.csn.edu")

            local_part = email.split('@')[0]
            if not ("." in local_part or local_part.isdigit()):
                return render_template('signup_student.html', errorMsg="Email must be first.last@student.csn.edu or nshe@student.csn.edu")

            if not nshe or not nshe.isdigit() or len(nshe) != 10:
                return render_template('signup_student.html', errorMsg="NSHE must be a 10-digit number")

            # Success (no DB persistence here) -> prompt to login
            flash("Signup successful! Please log in.", "success")
            # Redirect to the auth blueprint's login endpoint
            return redirect(url_for('auth.login'))

        # GET -> show the signup form
        return render_template('signup_student.html')
    except Exception:
        return jsonify({'error': 'template not available'}), 500


# Legacy compatibility: accept the alternate path '/student/signup' and delegate
# to the canonical signup_student view so old links or hard-coded forms still work.
@bp.route('/student/signup', methods=['GET', 'POST'])
def student_signup_alias():
    return signup_student()


@bp.route('/signup/faculty', methods=['GET'], endpoint='signup_faculty')
def signup_faculty():
    """Simple faculty signup/info page that directs users to the login flow."""
    try:
        return render_template('signup_faculty.html')
    except Exception:
        return jsonify({'error': 'template not available'}), 500


# Note: the canonical login route is provided by the `auth` blueprint.
@bp.route('/login', methods=['GET'], endpoint='login')
def login_page():
    """Render the HTML login page via the main blueprint as an alias.
    Primary login handling (POST) is implemented in `auth.login`.
    """
    try:
        return render_template('login.html')
    except Exception:
        return jsonify({'error': 'template not available'}), 500


# @bp.route('/student-signup', methods=['GET', 'POST'])
# def signup_student():
#     if request.method == 'POST':
#         first = request.form.get('first_name')
#         last = request.form.get('last_name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         nshe = request.form.get('nshe')
#         major = request.form.get('major')

#         # Validate email
#         if not email.endswith("@student.csn.edu"):
#             return render_template('signup_student.html', errorMsg="Email must end with @student.csn.edu")

#         local_part = email.split('@')[0]
#         if not ("." in local_part or local_part.isdigit()):
#             return render_template('signup_student.html', errorMsg="Email must be first.last@student.csn.edu or nshe@student.csn.edu")

#         # Validate NSHE number
#         if not nshe.isdigit() or len(nshe) != 10:
#             return render_template('signup_student.html', errorMsg="NSHE must be a 10-digit number")

#         # If everything is good
#         return render_template('signup_student.html', successMsg="Student signup successful!")

#     # GET request → show blank form
#     return render_template('signup_student.html')


# /homepage removed; root `/` (`Home`) is the canonical landing page (home.html)


@bp.route('/test-db')
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1')).scalar()
        return jsonify({'db_response': result})
    except Exception:
        logging.getLogger(__name__).exception("DB connectivity test failed")
        return jsonify({'error': 'database connection failed'}), 500


@bp.route('/__debug_index')
def debug_index():
    # Return on-disk index.html timestamp and a short preview for debugging
    tpl_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    try:
        mtime = os.path.getmtime(tpl_path)
        with open(tpl_path, 'r', encoding='utf-8') as f:
            preview = ''.join(f.readlines()[:120])
        return jsonify({
            'path': tpl_path,
            'modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime)),
            'preview_start': preview
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@bp.route('/__alive')
def alive():
    # Simple alive endpoint with timestamp so the client can verify the server is running this code
    return f"UPDATED: {int(time.time())}", 200


@bp.route('/preview')
def preview():
    """Return a standalone HTML page with inlined CSS from style.css to force-show the background.
    This bypasses template rendering and helps confirm the latest styles in the browser.
    """
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'css', 'style.css')
    bg_css_path = os.path.join(os.path.dirname(__file__), 'static', 'css', 'backgrounds.css')

    css = ''
    bg_css = ''
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css = f.read()
    except Exception:
        css = ''

    try:
        with open(bg_css_path, 'r', encoding='utf-8') as f:
            bg_css = f.read()
    except Exception:
        bg_css = ''

    # Inline both the main CSS and the background preview CSS for a single preview page
    html = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <title>Preview</title>
        <style>{css}\n{bg_css}</style>
    </head>
    <body>
    <div class="preview-grid" style="display:flex;gap:18px;align-items:stretch;justify-content:center;padding:24px;">
            <div class="preview-card bg-opt-1">
                <div class="preview-label">Brand-soft</div>
                <div class="preview-inner">
                    <div class="faceted"></div>
                    <div class="diagonal"></div>
                    <div class="vignette"></div>
                    <div class="login-box">
                        <input placeholder="Student Email" style="display:block;margin:8px 0;padding:10px;width:100%" />
                        <input placeholder="Password" style="display:block;margin:8px 0;padding:10px;width:100%" />
                        <button style="display:block;margin:12px auto;padding:8px 18px;border-radius:6px;background:var(--brand-accent);color:#fff;border:none">Login</button>
                    </div>
                </div>
            </div>

            <div class="preview-card bg-opt-2">
                <div class="preview-label">Hero-dramatic</div>
                <div class="preview-inner">
                    <div class="shard"></div>
                    <div class="grain"></div>
                    <div class="vignette"></div>
                    <div class="login-box" style="background:rgba(255,255,255,0.06);color:#fff">
                        <input placeholder="Student Email" style="display:block;margin:8px 0;padding:10px;width:100%" />
                        <input placeholder="Password" style="display:block;margin:8px 0;padding:10px;width:100%" />
                        <button style="display:block;margin:12px auto;padding:8px 18px;border-radius:6px;background:var(--brand-purple);color:#fff;border:none">Login</button>
                    </div>
                </div>
            </div>

            <div class="preview-card bg-opt-3">
                <div class="preview-label">Minimal-texture</div>
                <div class="preview-inner">
                    <div class="noise"></div>
                    <div class="vignette"></div>
                    <div class="login-box">
                        <input placeholder="Student Email" style="display:block;margin:8px 0;padding:10px;width:100%" />
                        <input placeholder="Password" style="display:block;margin:8px 0;padding:10px;width:100%" />
                        <button style="display:block;margin:12px auto;padding:8px 18px;border-radius:6px;background:var(--brand-accent);color:#fff;border:none">Login</button>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html