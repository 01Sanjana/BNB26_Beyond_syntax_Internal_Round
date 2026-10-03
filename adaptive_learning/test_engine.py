import unittest

from engine import get_intervention, evaluate_learning


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


if __name__ == "__main__":
    unittest.main()