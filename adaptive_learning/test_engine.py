import unittest

from adaptive_learning.engine import get_intervention, evaluate_learning

class TestReLearn(unittest.TestCase):

    def test_valid_intervention(self):
        intervention = get_intervention("reference_vs_copy")

        self.assertIsNotNone(intervention)
        self.assertEqual(
            intervention["title"],
            "Assignment creates a copy"
        )

    def test_invalid_intervention(self):
        intervention = get_intervention(
            "unknown_misconception"
        )

        self.assertIsNone(intervention)

    def test_persistent_learning(self):
        result = evaluate_learning(False, False)

        self.assertEqual(result, "persistent")

    def test_improving_learning(self):
        result = evaluate_learning(True, False)

        self.assertEqual(result, "improving")

    def test_resolved_learning(self):
        result = evaluate_learning(True, True)

        self.assertEqual(result, "resolved")
    
    def test_adaptive_intervention(self):
        from adaptive_learning.engine import learner

        learner.history.clear()

        first = get_intervention("reference_vs_copy")

        learner.record_result(
            "reference_vs_copy",
            "persistent"
        )

        learner.record_result(
            "reference_vs_copy",
            "persistent"
        )

        recurring = get_intervention("reference_vs_copy")

        self.assertNotEqual(
            first["explanation"],
            recurring["explanation"]
        )

    def test_support_levels_change_intervention(self):
        from adaptive_learning.engine import learner

        learner.history.clear()

        initial = get_intervention("reference_vs_copy")

        learner.record_result(
            "reference_vs_copy",
            "persistent"
        )

        reinforcement = get_intervention(
            "reference_vs_copy"
        )

        learner.record_result(
            "reference_vs_copy",
            "persistent"
        )

        guided = get_intervention(
            "reference_vs_copy"
        )

        learner.record_result(
            "reference_vs_copy",
            "improving"
        )

        transfer = get_intervention(
            "reference_vs_copy"
        )

        learner.record_result(
            "reference_vs_copy",
            "resolved"
        )

        mastery = get_intervention(
            "reference_vs_copy"
        )

        self.assertNotEqual(
            initial["explanation"],
            reinforcement["explanation"]
        )

        self.assertNotEqual(
            reinforcement["explanation"],
            guided["explanation"]
        )

        self.assertNotEqual(
            guided["explanation"],
            transfer["explanation"]
        )

        self.assertNotEqual(
            transfer["explanation"],
            mastery["explanation"]
        )

if __name__ == "__main__":
    unittest.main()