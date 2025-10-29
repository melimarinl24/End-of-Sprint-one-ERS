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

# ==========================================================
# TEMPORARY DEMO / PREVIEW ROUTE
# This route is ONLY for letting Melissa test the prefilled
# student info panel BEFORE the registration form is finished.
#
# When the teammate creates the real registration page, they
# will simply include:
#
#     {% include 'partials/student_prefill_form.html' %}
#
# inside the actual registration form.
# ==========================================================
@student_ui.route("/student/prefill-test", methods=["GET"])
@login_required
def student_prefill_test():
    return render_template("partials/student_prefill_form.html")
