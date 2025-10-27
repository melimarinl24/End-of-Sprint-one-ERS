from flask import Blueprint, Flask, request, jsonify, redirect, url_for, render_template
from project import create_app, db
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import os
import time
import logging

# --- import your models (adjust path/names if different) ---
from project.models import User, Role, Department, Major  # make sure these exist

student_ui = Blueprint("student_ui", __name__)

app = create_app()

# after app = create_app()
app.register_blueprint(student_ui)

# ---------- helpers ----------
def get_or_create(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    db.session.add(instance)
    db.session.flush()  # get .id
    return instance

def is_csn_student_email(email: str) -> bool:
    return email.endswith("@student.csn.edu")

def is_csn_faculty_email(email: str) -> bool:
    # adjust if your domain differs
    return email.endswith("@csn.edu") and not email.endswith("@student.csn.edu")

def is_10_digit_nshe(s: str) -> bool:
    return s and s.isdigit() and len(s) == 10

#  --------- Student Exam Scheduling --------------
# Student dashboard (landing after login)
@student_ui.route("/student/dashboard", methods=["GET"])
def student_dashboard():
# TODO: pull current user from session; guard with login_required
    return render_template("student/dashboard.html", user={"first_name": "Student"})


# Make an appointment → exam scheduling screen
@student_ui.route("/student/exams", methods=["GET"])
def student_exams():
# TODO: replace with DB query; static sample for now
    exam_list = [
        {"id": 101, "course": "MATH 126 - Precalculus II", "date": "2025-11-03", "time": "10:00 AM", "location": "Henderson Testing Ctr"},
        {"id": 202, "course": "CS 202 - Data Structures", "date": "2025-11-05", "time": "1:00 PM", "location": "Charleston Testing Ctr"},
    ]
    return render_template("student/schedule_exam.html", exams=exam_list)


# View my appointments
@student_ui.route("/student/appointments", methods=["GET"])
def student_appointments():
# TODO: replace with DB pull for this student
    appts = [
        {"appt_id": 1, "course": "CS 202 - Data Structures", "date": "2025-11-05", "time": "1:00 PM", "location": "Charleston"},
        {"appt_id": 2, "course": "MATH 126 - Precalculus II","date": "2025-11-03", "time": "10:00 AM", "location": "Henderson"},
    ]
    return render_template("student/appointments.html", appts=appts)


# Cancel/Reschedule (UI only; no DB mutation yet)
@student_ui.route("/student/appointments/<int:appt_id>/manage", methods=["GET"])
def manage_appointment(appt_id):
    # Typically you would fetch the appointment and show options
    return render_template("student/manage_appointment.html", appt_id=appt_id)

# ---------- keep your debug + db test endpoints ----------
@app.route('/__debug_index')
def debug_index():
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

@app.route('/test-db')
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1')).scalar()
        return jsonify({'db_response': result})
    except Exception as e:
        logging.getLogger(__name__).exception("DB connectivity test failed")
        return jsonify({'error': 'database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')
