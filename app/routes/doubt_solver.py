"""Doubt Solver — AI chat with watsonx.ai (session-based history)."""
from flask import Blueprint, render_template, request, jsonify, session
from app.core.watsonx_client import build_doubt_prompt, generate

doubt_bp = Blueprint("doubt", __name__)

BRANCHES = ["ECE", "CSE", "EEE", "MECH", "CIVIL", "IT"]


@doubt_bp.route("/")
def index():
    session.setdefault("chat_history", [])
    session.setdefault("chat_branch", "ECE")
    return render_template("doubt_solver.html", branches=BRANCHES)


@doubt_bp.route("/ask", methods=["POST"])
def ask():
    data     = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    branch   = (data.get("branch")   or "ECE").upper()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    history = session.get("chat_history", [])

    prompt = build_doubt_prompt(question, branch, history)
    result = generate(prompt, mode="general")

    if result["error"]:
        return jsonify({"error": result["error"]}), 503

    # Save to session history
    history.append({"role": "user",      "content": question})
    history.append({"role": "assistant", "content": result["text"]})
    session["chat_history"] = history[-30:]   # keep last 30 messages
    session["chat_branch"]  = branch

    return jsonify({
        "answer":     result["text"],
        "model_used": result["model_used"],
    })


@doubt_bp.route("/clear", methods=["POST"])
def clear():
    session.pop("chat_history", None)
    return jsonify({"status": "cleared"})
