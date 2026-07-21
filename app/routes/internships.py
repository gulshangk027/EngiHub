"""Internship Portal — JSON-backed listing with search & filters."""
import json
import os
from flask import Blueprint, render_template, request, jsonify

internship_bp = Blueprint("internship", __name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/internships.json")

BRANCHES   = ["All", "ECE", "CSE", "EEE", "MECH", "CIVIL", "IT"]
LOCATIONS  = ["All", "Remote", "Bangalore", "Hyderabad", "Mumbai", "Delhi", "Chennai", "Pune"]
TYPES      = ["All", "Paid", "Unpaid", "Stipend-based"]


def load_internships():
    try:
        abs_path = os.path.abspath(DATA_FILE)
        with open(abs_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[internships] ERROR loading internships.json: {e}")
        return []


@internship_bp.route("/")
def index():
    internships = load_internships()
    return render_template(
        "internships.html",
        internships=internships,
        branches=BRANCHES,
        locations=LOCATIONS,
        types=TYPES,
    )


@internship_bp.route("/filter", methods=["GET"])
def filter_internships():
    branch   = request.args.get("branch",   "All")
    location = request.args.get("location", "All")
    itype    = request.args.get("type",     "All")
    search   = request.args.get("search",   "").lower()

    data = load_internships()

    if branch   != "All": data = [i for i in data if branch   in i.get("branches", [])]
    if location != "All": data = [i for i in data if i.get("location") == location]
    if itype    != "All": data = [i for i in data if i.get("type") == itype]
    if search:
        data = [i for i in data if search in i.get("title", "").lower()
                                or search in i.get("company", "").lower()]

    return jsonify(data)
