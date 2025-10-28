# project/student_ui.py
from flask import Blueprint, render_template
from flask_login import login_required

student_ui = Blueprint("student_ui", __name__)

@student_ui.route('/student_dashboard')
@login_required
def student_dashboard():
    return render_template("student_dashboard.html")

@student_ui.route("/student/exams", methods=["GET"])
@login_required
def student_exams():
    return render_template("schedule_exam.html")

@student_ui.route("/student/appointments", methods=["GET"])
@login_required
def student_appointments():
    return render_template("appointments.html")
