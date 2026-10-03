class LearnerModel:
    """
    Tracks a student's misconception history and learning progress.
    """

    def __init__(self):
        self.history = {}

    def record_result(self, misconception, status):
        """
        Record a learning result for a misconception.
        """

        if misconception not in self.history:
            self.history[misconception] = {
                "attempts": 0,
                "status": None,
                "results": []
            }

        self.history[misconception]["attempts"] += 1
        self.history[misconception]["status"] = status
        self.history[misconception]["results"].append(status)

    def get_status(self, misconception):
        """
        Return the latest status for a misconception.
        """

        if misconception not in self.history:
            return "not_attempted"

        return self.history[misconception]["status"]

    def get_attempts(self, misconception):
        """
        Return the number of attempts for a misconception.
        """

        if misconception not in self.history:
            return 0

        return self.history[misconception]["attempts"]

    def is_recurring(self, misconception):
        """
        Return True if the misconception has appeared
        in two or more learning attempts.
        """

        return self.get_attempts(misconception) >= 2

    def get_progress(self):
        """
        Return the complete learner history.
        """

        return self.history