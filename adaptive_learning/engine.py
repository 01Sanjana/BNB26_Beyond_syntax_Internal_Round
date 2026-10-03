import json
from pathlib import Path


# Load our intervention knowledge base
DATA_FILE = Path(__file__).parent / "interventions.json"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    INTERVENTIONS = json.load(file)


def get_intervention(misconception):
    """
    Return the intervention for a detected misconception.
    """

    intervention = INTERVENTIONS.get(misconception)

    if intervention is None:
        return None

    return intervention


def evaluate_learning(diagnostic_correct, transfer_correct):
    """
    Decide whether the student's misconception is:
    - persistent
    - improving
    - resolved
    """

    if not diagnostic_correct:
        return "persistent"

    if not transfer_correct:
        return "improving"

    return "resolved"


def get_status_message(status):
    """
    Convert the internal status into a student-friendly message.
    """

    messages = {
        "persistent": "The concept still needs practice.",
        "improving": "You're improving, but let's practice this concept once more.",
        "resolved": "Great! Your understanding has been verified."
    }

    return messages[status]

def ask_question(question_data):
    """
    Display a multiple-choice question and return
    whether the student's answer is correct.
    """

    print("\n" + question_data["question"])

    for index, option in enumerate(question_data["options"], start=1):
        print(f"{index}. {option}")

    while True:
        try:
            answer = int(input("\nYour answer (1-4): "))

            if 1 <= answer <= len(question_data["options"]):
                return answer - 1 == question_data["correct"]

            print("Please choose a valid option.")

        except ValueError:
            print("Please enter a number.")


def run_learning_session(misconception):
    """
    Run a complete adaptive learning session.
    """

    intervention = get_intervention(misconception)

    if intervention is None:
        print("Misconception not found.")
        return

    print("\n================================")
    print("          RE:LEARN")
    print("================================")

    print("\nMisconception detected:")
    print(intervention["title"])

    print("\n--- Targeted Intervention ---")
    print(intervention["explanation"])

    print("\nExample:")
    print(intervention["example"]["code"])

    print("\nExpected output:")
    print(intervention["example"]["answer"])

    print("\n--- Diagnostic Question ---")

    diagnostic_correct = ask_question(
        intervention["diagnostic"]
    )

    if diagnostic_correct:
        print("\n✓ Correct! Let's see if you can apply it somewhere new.")

    else:
        print("\n✗ Not quite. Let's revisit the idea.")

        print("\n--- Reinforcement ---")
        print(intervention["reinforcement"])

        print("\n--- Diagnostic Retry ---")

        diagnostic_correct = ask_question(
            intervention["diagnostic"]
        )

        if diagnostic_correct:
            print("\n✓ Great! Your second attempt shows improvement.")

        else:
            print("\n✗ The misconception is still present.")

            print("\n================================")
            print("       LEARNING RESULT")
            print("================================")

            print("\nStatus: PERSISTENT")
            print("The concept still needs more practice.")

            return

    print("\n--- Transfer Question ---")

    transfer_correct = ask_question(
        intervention["transfer"]
    )

    status = evaluate_learning(
        diagnostic_correct,
        transfer_correct
    )

    print("\n================================")
    print("       LEARNING RESULT")
    print("================================")

    print("\nStatus:", status.upper())

    print(get_status_message(status))


if __name__ == "__main__":

    misconception = "reference_vs_copy"

    run_learning_session(misconception)