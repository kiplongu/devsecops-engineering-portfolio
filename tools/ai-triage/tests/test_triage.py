import importlib.util
import os
import pathlib
import unittest
from unittest.mock import patch


MODULE_PATH = pathlib.Path(__file__).parents[1] / "triage.py"
SPEC = importlib.util.spec_from_file_location("portfolio_ai_triage", MODULE_PATH)
TRIAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRIAGE)


class TriageTests(unittest.TestCase):
    def test_offline_mode_is_deterministic_and_requires_review(self):
        finding = {"id": "CVE-DEMO", "cvss": 9.8, "knownExploited": True,
                   "internetExposed": True, "reachable": True,
                   "assetCriticality": "critical", "fixAvailable": True}
        with patch.dict(os.environ, {}, clear=True):
            first = TRIAGE.run(finding)
            second = TRIAGE.run(finding)
        self.assertEqual(first, second)
        self.assertEqual(first["priority"], "critical")
        self.assertEqual(first["mode"], "offline-mock")
        self.assertTrue(first["humanReviewRequired"])
        self.assertEqual(first["decision"], "pending-human-review")

    def test_optional_model_cannot_override_priority(self):
        finding = {"id": "CVE-DEMO", "cvss": 4.0, "assetCriticality": "low"}
        with patch.object(TRIAGE, "llm_narrative", return_value=("Review this finding.", "optional-llm")):
            result = TRIAGE.run(finding)
        self.assertEqual(result["priority"], "low")
        self.assertEqual(result["decision"], "pending-human-review")
        self.assertEqual(result["analystNarrative"], "Review this finding.")


if __name__ == "__main__":
    unittest.main()
