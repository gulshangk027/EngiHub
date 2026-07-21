"""Placement Guidance — static content page."""
from flask import Blueprint, render_template

placement_bp = Blueprint("placement", __name__)


@placement_bp.route("/")
def index():
    return render_template("placement.html")
