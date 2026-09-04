import json
import unittest
from pathlib import Path

class CommonSchemasContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[3]
        cls.schemas_dir = cls.root / "contracts/schemas/common"
        cls.fixtures_dir = cls.root / "contracts/fixtures"

    def test_timestamp_schema_structure(self):
        schema_path = self.schemas_dir / "timestamp_v1.schema.json"
        self.assertTrue(schema_path.is_file(), "timestamp_v1.schema.json must exist")
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(data.get("$id"), "https://sih26168.invalid/contracts/schemas/common/timestamp_v1.schema.json")
        self.assertEqual(data.get("type"), "object")
        self.assertTrue(data.get("additionalProperties"), "Tier B schema must permit forward-compatible extension")
        self.assertEqual(set(data.get("required", [])), {"epoch_ns", "arrival_elapsed_realtime_ns", "clock_id"})
        # Enforce signed int64 nanosecond bounds
        for field in ("epoch_ns", "arrival_elapsed_realtime_ns", "source_timestamp_ns"):
            self.assertEqual(data["properties"][field].get("maximum"), 9223372036854775807, f"{field} must bound int64 max")

    def test_provenance_schema_structure(self):
        schema_path = self.schemas_dir / "provenance_v1.schema.json"
        self.assertTrue(schema_path.is_file(), "provenance_v1.schema.json must exist")
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(data.get("$id"), "https://sih26168.invalid/contracts/schemas/common/provenance_v1.schema.json")
        self.assertEqual(data.get("type"), "object")
        self.assertTrue(data.get("additionalProperties"), "Tier B schema must permit forward-compatible extension")
        self.assertEqual(set(data.get("required", [])), {"evidence_id", "session_id", "stream_id", "provenance_type"})
        self.assertEqual(set(data["properties"]["provenance_type"]["enum"]), {"LIVE_DEVICE", "DETERMINISTIC_REPLAY", "LIVE", "REPLAY"})
        self.assertIn("synthetic", data["properties"])
        self.assertGreaterEqual(data["properties"]["device_id"].get("minLength", 0), 1)
        self.assertGreaterEqual(data["properties"]["build_id"].get("minLength", 0), 1)

    def test_evidence_envelope_schema_structure(self):
        schema_path = self.schemas_dir / "evidence_envelope_v1.schema.json"
        self.assertTrue(schema_path.is_file(), "evidence_envelope_v1.schema.json must exist")
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(data.get("$id"), "https://sih26168.invalid/contracts/schemas/common/evidence_envelope_v1.schema.json")
        self.assertEqual(data.get("type"), "object")
        self.assertTrue(data.get("additionalProperties"), "Tier B schema must permit forward-compatible extension")
        self.assertEqual(set(data.get("required", [])), {"schema_version", "payload_type", "timestamp", "provenance", "payload", "validity_gate"})

    def test_common_envelope_fixture_validates(self):
        fixture_path = self.fixtures_dir / "common_envelope_v1_fixture.json"
        self.assertTrue(fixture_path.is_file(), "common_envelope_v1_fixture.json must exist")
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertEqual(fixture["schema_version"], 1)
        self.assertEqual(fixture["payload_type"], "RawSensorSample")
        self.assertGreater(fixture["timestamp"]["epoch_ns"], 0)
        self.assertGreater(fixture["timestamp"]["arrival_elapsed_realtime_ns"], 0)
        self.assertEqual(fixture["provenance"]["provenance_type"], "DETERMINISTIC_REPLAY")
        self.assertTrue(fixture["provenance"]["synthetic"])
        self.assertTrue(fixture["validity_gate"]["is_finite"])
        self.assertTrue(fixture["validity_gate"]["is_valid"])

        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed; skipping Draft 2020-12 fixture validation")

        envelope_schema = json.loads((self.schemas_dir / "evidence_envelope_v1.schema.json").read_text(encoding="utf-8"))
        timestamp_schema = json.loads((self.schemas_dir / "timestamp_v1.schema.json").read_text(encoding="utf-8"))
        provenance_schema = json.loads((self.schemas_dir / "provenance_v1.schema.json").read_text(encoding="utf-8"))

        # Verify meta-schema compliance
        jsonschema.Draft202012Validator.check_schema(timestamp_schema)
        jsonschema.Draft202012Validator.check_schema(provenance_schema)
        jsonschema.Draft202012Validator.check_schema(envelope_schema)

        # Validate fixture against envelope schema using a registry or RefResolver
        try:
            from referencing import Registry, Resource
            registry = (
                Registry()
                .with_resource("timestamp_v1.schema.json", Resource.from_contents(timestamp_schema))
                .with_resource("provenance_v1.schema.json", Resource.from_contents(provenance_schema))
                .with_resource(timestamp_schema["$id"], Resource.from_contents(timestamp_schema))
                .with_resource(provenance_schema["$id"], Resource.from_contents(provenance_schema))
            )
            validator = jsonschema.Draft202012Validator(envelope_schema, registry=registry)
            validator.validate(fixture)
        except ImportError:
            schema_store = {
                timestamp_schema["$id"]: timestamp_schema,
                provenance_schema["$id"]: provenance_schema,
                "timestamp_v1.schema.json": timestamp_schema,
                "provenance_v1.schema.json": provenance_schema,
            }
            resolver = jsonschema.RefResolver.from_schema(envelope_schema, store=schema_store)
            validator = jsonschema.Draft202012Validator(envelope_schema, resolver=resolver)
            validator.validate(fixture)

if __name__ == "__main__":
    unittest.main()
