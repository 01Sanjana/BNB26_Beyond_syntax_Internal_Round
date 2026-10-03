import unittest
import tempfile
from pathlib import Path

from adaptive_learning.learner_model import LearnerModel


class TestLearnerModel(unittest.TestCase):

    def setUp(self):
        self.learner = LearnerModel()
        self.learner.history.clear()
    
    def test_new_learner(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = LearnerModel(
                Path(temp_dir) / "test_history.json"
            )

        self.assertEqual(
            learner.get_status("reference_vs_copy"),
            "not_attempted"
        )

    def test_record_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = LearnerModel(
                Path(temp_dir) / "test_history.json"
            )

        learner.record_result(
            "reference_vs_copy",
            "improving"
        )

        self.assertEqual(
            learner.get_status("reference_vs_copy"),
            "improving"
        )

    def test_attempt_count(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = LearnerModel(
                Path(temp_dir) / "test_history.json"
            )

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
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = LearnerModel(
                Path(temp_dir) / "test_history.json"
            )

        learner.record_result(
            "print_vs_return",
            "resolved"
        )

        progress = learner.get_progress()

        self.assertIn(
            "print_vs_return",
            progress
        )

    def test_recurring_misconception(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = LearnerModel(
                Path(temp_dir) / "test_history.json"
            )

        learner.record_result(
            "reference_vs_copy",
            "persistent"
        )

        self.assertFalse(
            learner.is_recurring("reference_vs_copy")
        )

        learner.record_result(
            "reference_vs_copy",
            "persistent"
        )

        self.assertTrue(
            learner.is_recurring("reference_vs_copy")
        )

    def test_support_level(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            learner = LearnerModel(
                Path(temp_dir) / "test_history.json"
            )

        self.assertEqual(
            learner.get_support_level("reference_vs_copy"),
            "initial"
        )

        learner.record_result(
            "reference_vs_copy",
            "persistent"
        )

        self.assertEqual(
            learner.get_support_level("reference_vs_copy"),
            "reinforcement"
        )

        learner.record_result(
            "reference_vs_copy",
            "persistent"
        )

        self.assertEqual(
            learner.get_support_level("reference_vs_copy"),
            "guided"
        )

        learner.record_result(
            "reference_vs_copy",
            "improving"
        )

        self.assertEqual(
            learner.get_support_level("reference_vs_copy"),
            "transfer"
        )

        learner.record_result(
            "reference_vs_copy",
            "resolved"
        )

        self.assertEqual(
            learner.get_support_level("reference_vs_copy"),
            "mastery"
        )

if __name__ == "__main__":
    unittest.main()
