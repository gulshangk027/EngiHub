"""Main / Landing page routes."""
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

BRANCHES = ["ECE", "CSE", "EEE", "MECH", "CIVIL", "IT"]

@main_bp.route("/")
def index():
    return render_template("index.html", branches=BRANCHES)
