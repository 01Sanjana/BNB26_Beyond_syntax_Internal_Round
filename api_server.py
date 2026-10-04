from flask import Flask, request, jsonify
from flask_cors import CORS

from adaptive_learning.detector import detect_misconception
from adaptive_learning.engine import get_intervention, learner

from backend.code_analysis.analyzer import analyze_student_code
from backend.code_analysis.misconception_detector import detect_misconception as detect_code_misconception
from backend.code_analysis.intervention import generate_intervention

app = Flask(__name__)
CORS(app)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    code = data.get("code", "")
    expected_output = data.get("expected_output", "")
    student_output = data.get("student_output", "")

    misconception = detect_misconception(
        code,
        expected_output,
        student_output
    )

    if misconception is None:
        return jsonify({
            "correct": True,
            "misconception": None,
            "confidence": 1.0,
            "evidence": "No known misconception detected.",
            "intervention": None
        })

    intervention = get_intervention(misconception)

    return jsonify({
        "correct": False,
        "misconception": intervention["title"],
        "misconception_id": misconception,
        "confidence": 0.87,
        "evidence": intervention["explanation"],
        "intervention": intervention
    })

@app.route("/analyze_code", methods=["POST"])
def analyze_code():
    data = request.get_json(silent=True) or {}

    code = data.get("code", "")

    if not code.strip():
        return jsonify({
            "success": False,
            "error": "Please provide Python code."
        }), 400

    # Step 1: Analyze code structure and execution
    analysis = analyze_student_code(code)

    # Step 2: Detect possible misconception
    misconception = detect_code_misconception(analysis)

    # Step 3: Generate personalized intervention
    intervention = generate_intervention(misconception)

    return jsonify({
        "success": True,
        "analysis": analysis,
        "misconception": misconception,
        "intervention": intervention
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
