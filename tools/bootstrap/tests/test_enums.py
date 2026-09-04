import json
import unittest
from pathlib import Path

class EnumsContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[3]
        cls.enums_dir = cls.root / "contracts/enums"

    def test_navigation_states_v1(self):
        file_path = self.enums_dir / "navigation_states_v1.json"
        self.assertTrue(file_path.is_file())
        data = json.loads(file_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("schema_version"), 1)
        self.assertNotIn("note", data, "Scaffold note must be removed")
        expected_states = ["INITIALIZING", "GNSS_AIDED", "DEGRADED", "BLACKOUT_DR", "REACQUIRING", "FAULT"]
        self.assertEqual(data.get("navigation_states"), expected_states)
        self.assertIn("SYNTHETIC", data.get("provenance", []))

    def test_navigation_mode_v1(self):
        file_path = self.enums_dir / "navigation_mode_v1.json"
        self.assertTrue(file_path.is_file())
        data = json.loads(file_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("enum_name"), "NavigationModeV1")
        expected = ["INITIALIZING", "GNSS_AIDED", "DEGRADED", "BLACKOUT_DR", "REACQUIRING", "FAULT"]
        self.assertEqual(data.get("values"), expected)
        # Check transition graph completeness
        for mode in expected:
            self.assertIn(mode, data.get("definitions", {}))

    def test_health_integrity_v1(self):
        file_path = self.enums_dir / "health_integrity_v1.json"
        self.assertTrue(file_path.is_file())
        data = json.loads(file_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("enum_name"), "HealthIntegrityStateV1")
        expected = ["HEALTHY", "DEGRADED", "FAILED", "UNAVAILABLE", "OUTAGE", "REACQUISITION_PENDING", "REACQUIRED"]
        self.assertEqual(data.get("values"), expected)

    def test_alignment_status_v1(self):
        file_path = self.enums_dir / "alignment_status_v1.json"
        self.assertTrue(file_path.is_file())
        data = json.loads(file_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("enum_name"), "AlignmentStatusV1")
        expected = ["UNALIGNED", "COARSE_ALIGNING", "FINE_ALIGNING", "ALIGNED", "MOUNT_SLIP_DETECTED", "REALIGNING"]
        self.assertEqual(data.get("values"), expected)

    def test_display_mode_v1(self):
        file_path = self.enums_dir / "display_mode_v1.json"
        self.assertTrue(file_path.is_file())
        data = json.loads(file_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("enum_name"), "DisplayModeV1")
        expected = ["LIVE_ACTIVE", "LIVE_DEGRADED", "LIVE_BLACKOUT", "REPLAY_ACTIVE", "REPLAY_PAUSED", "STALE", "FAULT"]
        self.assertEqual(data.get("values"), expected)

    def test_enum_invariants(self):
        for json_file in self.enums_dir.glob("*.json"):
            data = json.loads(json_file.read_text(encoding="utf-8"))
            if "values" in data:
                values = data["values"]
                self.assertIsInstance(values, list)
                self.assertEqual(len(values), len(set(values)), f"Duplicate enum values in {json_file.name}")
                for val in values:
                    self.assertIsInstance(val, str)
                    self.assertTrue(val.isupper(), f"Enum {val} in {json_file.name} must be uppercase")

if __name__ == "__main__":
    unittest.main()
