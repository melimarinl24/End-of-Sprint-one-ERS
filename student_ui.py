# project/student_ui.py
from flask import Blueprint, render_template

student_ui = Blueprint("student_ui", __name__)

# Student dashboard (landing after login; optional)
@student_ui.route("/student/dashboard", methods=["GET"])
def student_dashboard():
    # You can pass a real user later
    return render_template("dashboard.html")

# Make an appointment
@student_ui.route("/student/exams", methods=["GET"])
def student_exams():
    # TODO: real template; temporary stub keeps things working
    return render_template("schedule_exam.html")

# View my appointments
@student_ui.route("/student/appointments", methods=["GET"])
def student_appointments():
    # TODO: real template; temporary stub keeps things working
    return render_template("appointments.html")
