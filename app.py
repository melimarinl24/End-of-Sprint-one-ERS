from flask import Flask, request, jsonify, redirect, url_for, render_template
from project import create_app, db
from sqlalchemy import text
import os
import time
import logging

app = create_app()

@app.route('/', methods=['GET'])
def home():
    # Clear Jinja template cache for development so updated templates are picked up
    try:
        app.jinja_env.cache.clear()
    except Exception:
        pass
    # Root now serves the hero homepage
    return render_template('home.html')

@app.route('/home', methods=['GET'])
# REDIRECT LATER
def redirect_home():
    return redirect(url_for('home'))

@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name  = request.form.get("last_name")
        email      = request.form.get("email")
        phone      = request.form.get("phone")
        nshe       = request.form.get("nshe")
        major      = request.form.get("major")

        # TODO: validate + insert into DB
        # For now we just confirm:
        successMsg = "Student account created for " + (first_name or '') + " " + (last_name or '')
        # Use the template at templates/signup_student.html
        return render_template('signup_student.html', successMsg=successMsg)

    # GET -> show the signup form (template lives at templates/signup_student.html)
    return render_template('signup_student.html')


# @app.route('/student/signup', methods=['GET'])
# def student_signup():
#      return render_template('/signup_student.html')


@app.route('/faculty-signup', methods=['GET'])
def faculty_signup():
    try:
        app.jinja_env.cache.clear()
    except Exception:
        pass

    # Redirect /home to root
    try:
        app.jinja_env.cache.clear()
    except Exception:
        pass
    return render_template('faculty_signup.html')

# @app.route('/', methods=['GET'])
# def home():
#     # Clear Jinja template cache for development so updated templates are picked up
#     try:
#         app.jinja_env.cache.clear()
#     except Exception:
#         pass
#     # Root now serves the hero homepage
#     return render_template('home.html')


# @app.route('/home', methods=['GET'])
# def homepage():
#     try:
#         app.jinja_env.cache.clear()
#     except Exception:
#         pass
#     # Redirect /home to root
#     try:
#         app.jinja_env.cache.clear()
#     except Exception:
#         pass
#     return render_template('home.html')


@app.route('/__debug_index')
def debug_index():
    # Return on-disk index.html timestamp and a short preview of its contents for debugging
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

@app.route('/signup', methods=['GET'])
def Signup():
    return jsonify({'message': 'Sign up'})


# Note: the HTML login page is provided by the blueprint (project.views)

@app.route('/test-db')
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1')).scalar()
        return jsonify({'db_response': result})
    except Exception as e:
        # log the exception server-side for diagnostics, but return a generic error to clients
        logging.getLogger(__name__).exception("DB connectivity test failed")
        return jsonify({'error': 'database connection failed'}), 500


# To run the application, save this code in a file named app.py and execute it with Python.
# Then, navigate to http://
#localhost:5000/ in your web browser to see the output.

if __name__ == '__main__':
    # For local development we bind to localhost only and disable the interactive debugger.
    # This prevents the debug console from being exposed to remote clients.
    app.run(debug=False, host='127.0.0.1')