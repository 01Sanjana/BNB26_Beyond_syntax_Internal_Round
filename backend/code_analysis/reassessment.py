def check_answer(user_answer, correct_answer):

    if user_answer.strip().lower() == correct_answer.strip().lower():
        return {
            "correct": True,
            "status": "MISCONCEPTION_RESOLVED",
            "message": "Correct! The concept appears to be understood."
        }

    return {
        "correct": False,
        "status": "MISCONCEPTION_PERSISTS",
        "message": "The misconception may still be present. Another explanation or example is needed."
    }