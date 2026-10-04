from .misconception_detector import detect_misconception
from .intervention import generate_intervention
from .reassessment import check_answer


def run_learning_flow(analysis, student_answer, correct_answer):
    """
    Run the complete adaptive learning process.

    Args:
        analysis: Evidence produced by analyze_student_code().
        student_answer: Student's response to the check question.
        correct_answer: Expected answer.

    Returns:
        A dictionary containing the detected misconception,
        personalized intervention, and reassessment result.
    """

    # Step 1: Detect misconception using analysis evidence
    misconception = detect_misconception(analysis)

    # Step 2: Generate a personalized intervention
    intervention = generate_intervention(misconception)

    # Step 3: Reassess the student's understanding
    reassessment = check_answer(
        student_answer,
        correct_answer
    )

    # Step 4: Return the complete learning result
    return {
        "misconception": misconception,
        "intervention": intervention,
        "reassessment": reassessment
    }