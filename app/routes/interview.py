"""Interview Prep — static question bank + AI live mock question generator."""
import json
import os
from flask import Blueprint, render_template, request, jsonify
import re
from app.core.watsonx_client import build_interview_prompt, build_qbank_batch_prompt, generate

interview_bp = Blueprint("interview", __name__)

BRANCHES     = ["ECE", "CSE", "EEE", "MECH", "CIVIL", "IT"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]

import logging

logger = logging.getLogger(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/interview_qbank.json")

# In-memory cache for generated topic questions during session
QBANK_CACHE = {}


def load_qbank():
    try:
        abs_path = os.path.abspath(DATA_FILE)
        with open(abs_path, encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"Failed to load interview_qbank.json: {e}")
        print(f"[interview] ERROR loading interview_qbank.json: {e}")
        return {}


def parse_ai_questions(text: str, default_diff: str, default_branch: str) -> list:
    """Parse raw watsonx.ai output into structured question-answer dictionaries."""
    questions = []
    raw_blocks = re.split(r"(?:^|\n)(?:Q\d*:|\d+\.\s*Q:|\d+\.\s+Question:)", text, flags=re.I)
    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue
        parts = re.split(r"(?:^|\n)(?:A\d*:|Answer:|Model Answer:)", block, maxsplit=1, flags=re.I)
        if len(parts) == 2:
            q_text = parts[0].strip()
            a_text = parts[1].strip()
            a_text = re.sub(r"\n*---.*$", "", a_text, flags=re.S).strip()
            q_text = re.sub(r"^\**[0-9.]*\s*", "", q_text).strip()
            if len(q_text) >= 8 and len(a_text) >= 5:
                questions.append({
                    "q": q_text,
                    "answer": a_text,
                    "difficulty": default_diff if default_diff != "All" else "Medium",
                    "branch": default_branch if default_branch != "All" else "ECE",
                    "is_ai": True
                })
        elif len(parts) == 1 and "?" in block:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if lines:
                q_text = lines[0]
                a_text = " ".join(lines[1:]) if len(lines) > 1 else "Refer to standard engineering textbooks and documentation."
                questions.append({
                    "q": q_text,
                    "answer": a_text,
                    "difficulty": default_diff if default_diff != "All" else "Medium",
                    "branch": default_branch if default_branch != "All" else "ECE",
                    "is_ai": True
                })
    return questions


@interview_bp.route("/")
def index():
    qbank = load_qbank()
    return render_template(
        "interview.html",
        branches=BRANCHES,
        difficulties=DIFFICULTIES,
        qbank=qbank,
    )


@interview_bp.route("/debug")
def debug():
    abs_path = os.path.abspath(DATA_FILE)
    qbank = load_qbank()
    total_q = sum(len(b.get("questions", [])) for b in qbank.values()) if isinstance(qbank, dict) else 0
    return jsonify({
        "data_file": abs_path,
        "exists": os.path.exists(abs_path),
        "branch_count": len(qbank),
        "total_questions": total_q,
        "branches": list(qbank.keys()) if isinstance(qbank, dict) else [],
    })


@interview_bp.route("/search", methods=["POST"])
def search_qbank():
    data = request.get_json(force=True) or {}
    topic = (data.get("topic") or "").strip()
    branch = (data.get("branch") or "All").strip()
    difficulty = (data.get("difficulty") or "").strip()

    if not topic:
        return jsonify({"error": "Topic parameter is required."}), 400

    qbank = load_qbank()
    query_lower = topic.lower()

    # 1. Search static JSON questions
    static_matches = []
    for b_name, b_data in qbank.items():
        if branch != "All" and b_name.upper() != branch.upper():
            continue
        for q in b_data.get("questions", []):
            if difficulty and q.get("difficulty") != difficulty:
                continue
            if (query_lower in q.get("q", "").lower() or 
                query_lower in q.get("answer", "").lower() or 
                any(query_lower in t.lower() for t in b_data.get("topics", []))):
                static_matches.append({
                    "q": q["q"],
                    "answer": q["answer"],
                    "difficulty": q.get("difficulty", "Medium"),
                    "branch": b_name,
                    "is_ai": False
                })

    # 2. Check session/in-memory cache
    cache_key = f"{branch}_{difficulty}_{query_lower}"
    if cache_key in QBANK_CACHE:
        logger.info(f"Returning cached AI questions for key: {cache_key}")
        return jsonify({
            "static_questions": static_matches,
            "ai_questions": QBANK_CACHE[cache_key],
            "source": "cache",
            "model_used": "Granite 8B (Cached)"
        })

    # 3. Generate new AI questions via watsonx.ai
    prompt = build_qbank_batch_prompt(branch, topic, difficulty or "Medium")
    res = generate(prompt, params={"max_new_tokens": 1000}, mode="qbank_batch")

    if res.get("error"):
        return jsonify({
            "static_questions": static_matches,
            "ai_questions": [],
            "source": "static_only",
            "error": res["error"],
            "model_used": res.get("model_used")
        })

    ai_questions = parse_ai_questions(res.get("text", ""), difficulty, branch)
    
    # Store in cache
    QBANK_CACHE[cache_key] = ai_questions

    return jsonify({
        "static_questions": static_matches,
        "ai_questions": ai_questions,
        "source": "ai",
        "model_used": res.get("model_used", "Granite 8B")
    })


@interview_bp.route("/generate-question", methods=["POST"])
def generate_question():
    data       = request.get_json(force=True)
    branch     = (data.get("branch")     or "ECE").strip()
    topic      = (data.get("topic")      or "General").strip()
    difficulty = (data.get("difficulty") or "Medium").strip()

    prompt = build_interview_prompt(branch, topic, difficulty)
    result = generate(prompt, params={"max_new_tokens": 600}, mode="interview")

    if result["error"]:
        return jsonify({"error": result["error"]}), 503

    return jsonify({
        "question":   result["text"],
        "model_used": result["model_used"],
    })

