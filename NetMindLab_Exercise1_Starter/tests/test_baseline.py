import json
import tempfile
import unittest
from pathlib import Path

from main import build_delay_models
from network_explorer.performance import propagation_delay, transmission_delay
from network_explorer.probes import ping
from network_explorer.report import save_json


class StarterTests(unittest.TestCase):
    def test_transmission_delay(self):
        self.assertAlmostEqual(transmission_delay(12000, 10_000_000), 0.0012)

    def test_propagation_delay(self):
        self.assertAlmostEqual(propagation_delay(100_000), 0.0005)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            transmission_delay(1, 0)

    def test_disallowed_target(self):
        with self.assertRaises(ValueError):
            ping("192.168.1.1")

    def test_json(self):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "result.json")
            save_json({"group_id": "NML-G001"}, path)
            self.assertEqual(
                json.loads(Path(path).read_text(encoding="utf-8"))["group_id"],
                "NML-G001",
            )

    def test_delay_model_schema_has_nodal_integration_point(self):
        models = build_delay_models()
        self.assertIn("nodal_s", models)
        self.assertIn("transmission_s", models)
        self.assertIn("propagation_s", models)


    def test_genai_reflection_template_schema(self):
        import json
        from pathlib import Path
        path = Path("results/genai_reflection.json")
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "1.0")
        self.assertEqual(data["exercise_id"], "NET-EX1-2026")
        self.assertEqual(len(data["claims"]), 2)
        for claim in data["claims"]:
            for key in (
                "claim_id", "claim_text", "initial_confidence_1_to_5",
                "evidence_type", "evidence_reference", "verification_result",
                "challenged_ai", "follow_up_question_asked",
                "interpretation_changed_after_verification",
                "final_confidence_1_to_5", "final_decision", "justification",
            ):
                self.assertIn(key, claim)

if __name__ == "__main__":
    unittest.main()
