"""Career Advisory — form → watsonx.ai → personalized roadmap."""
from flask import Blueprint, render_template, request, jsonify
from app.core.watsonx_client import build_career_prompt, generate

career_bp = Blueprint("career", __name__)

BRANCHES   = ["ECE", "CSE", "EEE", "MECH", "CIVIL", "IT"]
GOALS      = [
    "Software Development", "Research & Academia", "Core Engineering",
    "Product Management", "Entrepreneurship", "Government / PSU",
    "Higher Studies (MS/MTech)", "Data Science / AI",
]


@career_bp.route("/")
def index():
    return render_template("career.html", branches=BRANCHES, goals=GOALS)


@career_bp.route("/generate", methods=["POST"])
def generate_roadmap():
    data      = request.get_json(force=True)
    branch    = (data.get("branch")    or "ECE").strip()
    interests = (data.get("interests") or "").strip()
    skills    = (data.get("skills")    or "").strip()
    goal      = (data.get("goal")      or "").strip()

    if not interests or not goal:
        return jsonify({"error": "Please fill in all fields."}), 400

    prompt = build_career_prompt(branch, interests, skills, goal)
    result = generate(prompt, params={"max_new_tokens": 1500}, mode="career")

    if result["error"]:
        return jsonify({"error": result["error"]}), 503

    return jsonify({
        "roadmap":    result["text"],
        "model_used": result["model_used"],
    })
