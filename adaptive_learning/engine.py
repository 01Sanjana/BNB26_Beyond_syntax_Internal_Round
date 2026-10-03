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

if __name__ == "__main__":

    misconception = "reference_vs_copy"

    intervention = get_intervention(misconception)

    if intervention:
        print("\n--- Re:Learn Intervention ---")
        print("Misconception:", intervention["title"])
        print("\nExplanation:")
        print(intervention["explanation"])

        print("\nDiagnostic Question:")
        print(intervention["diagnostic"]["question"])

        print("\nTransfer Question:")
        print(intervention["transfer"]["question"])

        # Temporary test
        status = evaluate_learning(
            diagnostic_correct=True,
            transfer_correct=True
        )

        print("\nLearning Status:", status)
        print(get_status_message(status))

    else:
        print("Misconception not found.")