from misconception_detector import detect_misconception
from intervention import generate_intervention
from reassessment import check_answer


def run_learning_flow(analysis, student_answer, correct_answer):

    # Step 1: Detect misconception
    misconception = detect_misconception(analysis)

    # Step 2: Generate intervention
    intervention = generate_intervention(misconception)

    # Step 3: Reassess student
    reassessment = check_answer(
        student_answer,
        correct_answer
    )

    return {
        "misconception": misconception,
        "intervention": intervention,
        "reassessment": reassessment
    }