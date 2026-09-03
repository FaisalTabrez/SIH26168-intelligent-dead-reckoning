import json
import unittest
from pathlib import Path

class BootstrapSmokeTest(unittest.TestCase):
    def test_synthetic_fixture_is_replay_labeled(self):
        root = Path(__file__).resolve().parents[3]
        fixture = json.loads((root / "contracts/fixtures/synthetic_replay_event_v1.json").read_text())
        self.assertEqual(fixture["provenance"], "REPLAY")
        self.assertTrue(fixture["synthetic"])

if __name__ == "__main__":
    unittest.main()
