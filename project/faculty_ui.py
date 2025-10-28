# project/faculty_ui.py
from flask import Blueprint, render_template
from flask_login import login_required

faculty_ui = Blueprint("faculty_ui", __name__)

@faculty_ui.route("/faculty/dashboard", methods=["GET"])
@login_required
def faculty_dashboard():
    return render_template("faculty_dashboard.html")
