import json
from pathlib import Path


HISTORY_FILE = Path(__file__).parent / "learner_history.json"


class LearnerModel:
    """
    Tracks a student's misconception history and learning progress.
    """

    def __init__(self, history_file=None, load_existing=True):
        self.history = {}

        if history_file is None:
            self.history_file = HISTORY_FILE
        else:
            self.history_file = Path(history_file)

        if load_existing:
            self.load_history()

    def record_result(self, misconception, status):
        if misconception not in self.history:
            self.history[misconception] = {
                "attempts": 0,
                "status": None,
                "results": []
            }

        self.history[misconception]["attempts"] += 1
        self.history[misconception]["status"] = status
        self.history[misconception]["results"].append(status)

        self.save_history()

    def get_status(self, misconception):
        if misconception not in self.history:
            return "not_attempted"

        return self.history[misconception]["status"]

    def get_attempts(self, misconception):
        if misconception not in self.history:
            return 0

        return self.history[misconception]["attempts"]

    def is_recurring(self, misconception):
        return self.get_attempts(misconception) >= 2

    def get_support_level(self, misconception):
        attempts = self.get_attempts(misconception)
        status = self.get_status(misconception)

        if attempts == 0:
            return "initial"

        if status == "resolved":
            return "mastery"

        if status == "improving":
            return "transfer"

        if attempts == 1:
            return "reinforcement"

        return "guided"

    def get_progress(self):
        return self.history

    def save_history(self):
        self.history_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(self.history, file, indent=2)

    def load_history(self):
        if not self.history_file.exists():
            return

        try:
            with open(self.history_file, "r", encoding="utf-8") as file:
                self.history = json.load(file)

        except (json.JSONDecodeError, OSError):
            self.history = {}