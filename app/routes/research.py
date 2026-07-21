"""Research Hub — curated papers and tools by branch."""
import json
import os
import logging
from flask import Blueprint, render_template, request, jsonify

research_bp = Blueprint("research", __name__)
logger = logging.getLogger(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/research.json")

BRANCHES = ["All", "ECE", "CSE", "EEE", "MECH", "CIVIL", "IT"]
TYPES    = ["All", "Paper", "Article", "Tool", "Dataset", "Course"]


def load_research():
    try:
        abs_path = os.path.abspath(DATA_FILE)
        logger.info(f"Loading research data from: {abs_path}")
        with open(abs_path, encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} research items")
        return data
    except Exception as e:
        logger.error(f"Failed to load research.json: {e}")
        print(f"[research] ERROR loading research.json: {e}")
        return []


@research_bp.route("/")
def index():
    items = load_research()
    return render_template(
        "research.html",
        items=items,
        branches=BRANCHES,
        types=TYPES,
    )


@research_bp.route("/filter", methods=["GET"])
def filter_research():
    branch  = request.args.get("branch", "All")
    rtype   = request.args.get("type",   "All")
    search  = request.args.get("search", "").lower().strip()

    data = load_research()
    print(f"[research] filter: branch={branch!r} type={rtype!r} search={search!r} total={len(data)}")

    if branch != "All":
        data = [r for r in data if r.get("branch", "").strip() == branch.strip()]
        print(f"[research] after branch filter: {len(data)} items")
    if rtype  != "All":
        data = [r for r in data if r.get("type", "").strip() == rtype.strip()]
        print(f"[research] after type filter: {len(data)} items")
    if search:
        data = [r for r in data if search in r.get("title", "").lower()
                                 or search in r.get("description", "").lower()]
        print(f"[research] after search filter: {len(data)} items")

    return jsonify(data)


@research_bp.route("/debug")
def debug():
    """Debug endpoint — shows file path and raw loaded data count."""
    abs_path = os.path.abspath(DATA_FILE)
    exists = os.path.exists(abs_path)
    data = load_research()
    return jsonify({
        "data_file_path": abs_path,
        "file_exists": exists,
        "item_count": len(data),
        "branch_values": list({r.get("branch") for r in data}),
        "type_values":   list({r.get("type")   for r in data}),
    })

