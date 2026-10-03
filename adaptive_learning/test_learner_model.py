import unittest

from adaptive_learning.learner_model import LearnerModel


class TestLearnerModel(unittest.TestCase):

    def test_new_learner(self):
        learner = LearnerModel()

        self.assertEqual(
            learner.get_status("reference_vs_copy"),
            "not_attempted"
        )

    def test_record_result(self):
        learner = LearnerModel()

        learner.record_result(
            "reference_vs_copy",
            "improving"
        )

        self.assertEqual(
            learner.get_status("reference_vs_copy"),
            "improving"
        )

    def test_attempt_count(self):
        learner = LearnerModel()

        learner.record_result(
            "off_by_one",
            "persistent"
        )

        learner.record_result(
            "off_by_one",
            "improving"
        )

        self.assertEqual(
            learner.get_attempts("off_by_one"),
            2
        )

    def test_progress(self):
        learner = LearnerModel()

        learner.record_result(
            "print_vs_return",
            "resolved"
        )

        progress = learner.get_progress()

        self.assertIn(
            "print_vs_return",
            progress
        )


if __name__ == "__main__":
    unittest.main()