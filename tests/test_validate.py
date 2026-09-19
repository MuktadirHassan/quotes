import copy
import json
import unittest
from pathlib import Path

from scripts.validate import document_errors, schema_path_for

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schemas" / "v1.0.0.json").read_text(encoding="utf-8"))


def quote(quote_id: str = "example-quote-001") -> dict:
    return {
        "id": quote_id,
        "text": "Example text.",
        "attributedTo": "Example Person",
        "source": {"type": "book", "title": "Example Book"},
        "language": "en",
        "tags": ["example"],
        "verification": {"status": "unverified"},
    }


def collection(quotes: list[dict]) -> dict:
    return {
        "$schema": SCHEMA["$id"],
        "schemaVersion": "1.0.0",
        "datasetVersion": "0.0.0",
        "quotes": quotes,
    }


class ValidatorTests(unittest.TestCase):
    def test_accepts_valid_quote(self):
        self.assertEqual(document_errors(collection([quote()]), SCHEMA), [])

    def test_rejects_duplicate_ids(self):
        errors = document_errors(collection([quote(), quote()]), SCHEMA)
        self.assertTrue(any("duplicate quote id" in error for error in errors))

    def test_verified_quote_requires_evidence(self):
        item = quote()
        item["verification"] = {"status": "verified"}
        errors = document_errors(collection([item]), SCHEMA)
        self.assertTrue(any("evidenceUrl" in error for error in errors))

    def test_rejects_schema_version_mismatch(self):
        data = collection([quote()])
        data["schemaVersion"] = "2.0.0"
        errors = document_errors(data, SCHEMA)
        self.assertTrue(any("schemaVersion" in error for error in errors))

    def test_requires_schema_version(self):
        data = copy.deepcopy(collection([]))
        del data["schemaVersion"]
        with self.assertRaisesRegex(ValueError, "schemaVersion"):
            schema_path_for(data)


if __name__ == "__main__":
    unittest.main()
