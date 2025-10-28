print(">>> LOADED: views.py blueprint <<<")

from flask import Blueprint, render_template, jsonify, current_app, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from sqlalchemy import text
import os
import time
import logging

bp = Blueprint('main', __name__)


# views.py
@bp.route('/', methods=['GET', 'POST'], endpoint='home')
def home():
    if request.method == 'POST':
        # If a form accidentally posts to '/', bounce it to login (or wherever makes sense)
        return redirect(url_for('auth.login'))
    return render_template('home.html')


@bp.route('/dashboard')
# @login_required  # remove this for now if you haven't wired login_user yet
def dashboard():
    # If you have roles on the user, you can pass them to the template:
    role_name = getattr(getattr(current_user, 'role', None), 'name', None)
    return render_template('dashboard.html', role=role_name)

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