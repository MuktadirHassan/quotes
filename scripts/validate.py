#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parent.parent


def read_json(path: Path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def schema_path_for(collection: dict) -> Path:
    version = collection.get("schemaVersion")
    if not isinstance(version, str) or not version:
        raise ValueError("quotes.json must contain a schemaVersion string.")
    return ROOT / "schemas" / f"v{version}.json"


def document_errors(collection: dict, schema: dict) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []

    for error in sorted(validator.iter_errors(collection), key=lambda item: [str(part) for part in item.path]):
        location = "/" + "/".join(str(part) for part in error.path)
        errors.append(f"{location}: {error.message}")

    if collection.get("$schema") != schema.get("$id"):
        errors.append("/$schema: does not match the local schema $id")

    seen_ids = set()
    quotes = collection.get("quotes")
    if isinstance(quotes, list):
        for quote in quotes:
            if not isinstance(quote, dict):
                continue
            quote_id = quote.get("id")
            if quote_id in seen_ids:
                errors.append(f"/quotes: duplicate quote id: {quote_id}")
            seen_ids.add(quote_id)

    return errors


def main() -> int:
    try:
        collection = read_json(ROOT / "quotes.json")
        if not isinstance(collection, dict):
            raise ValueError("quotes.json must contain a JSON object.")
        schema_path = schema_path_for(collection)
        if not schema_path.is_file():
            raise ValueError(f"Missing schema: {schema_path.relative_to(ROOT)}")

        schema = read_json(schema_path)
        Draft202012Validator.check_schema(schema)

        manifest_path = ROOT / ".release-please-manifest.json"
        version_path = ROOT / "version.txt"
        if not manifest_path.is_file():
            raise ValueError("Missing .release-please-manifest.json")
        if not version_path.is_file():
            raise ValueError("Missing version.txt")

        manifest = read_json(manifest_path)
        manifest_version = manifest.get(".")
        if not isinstance(manifest_version, str) or not manifest_version:
            raise ValueError(".release-please-manifest.json must contain a version for '.'.")

        release_version = version_path.read_text(encoding="utf-8").strip()
        if not release_version:
            raise ValueError("version.txt must contain a version.")

        errors = document_errors(collection, schema)
        if errors:
            print(f"quotes.json does not match {schema_path.relative_to(ROOT)}:", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
            return 1

        versions = {
            "quotes.json": collection["datasetVersion"],
            "version.txt": release_version,
            ".release-please-manifest.json": manifest_version,
        }
        if len(set(versions.values())) != 1:
            values = ", ".join(f"{name}={version}" for name, version in versions.items())
            raise ValueError(f"Version mismatch: {values}")

    except (OSError, ValueError, KeyError, SchemaError, json.JSONDecodeError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(collection['quotes'])} quote(s) against schema "
        f"{collection['schemaVersion']} (dataset {collection['datasetVersion']})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
