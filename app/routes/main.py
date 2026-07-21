from flask import Blueprint, render_template, send_from_directory, current_app

main_bp = Blueprint("main", __name__)

BRANCHES = ["ECE", "CSE", "EEE", "MECH", "CIVIL", "IT"]

@main_bp.route("/")
def index():
    return render_template("index.html", branches=BRANCHES)

@main_bp.route("/sw.js")
def serve_sw():
    return send_from_directory(current_app.static_folder, "sw.js", mimetype="application/javascript")

@main_bp.route("/manifest.json")
def serve_manifest():
    return send_from_directory(current_app.static_folder, "manifest.json", mimetype="application/json")

