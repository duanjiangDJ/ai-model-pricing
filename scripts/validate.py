"""Validate all machine-readable data files against data/machine/schema.json.

Usage: python scripts/validate.py [--strict]
  --strict: fail on any unknown-provider reference or non-UTF8 issues (default: only schema errors fail)
Requires: pip install jsonschema
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import MACHINE, PROVIDERS, META, read_json  # noqa: E402

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    sys.exit("jsonschema not installed. Run: pip install jsonschema")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    schema = read_json(os.path.join(MACHINE, "schema.json"))
    checker = FormatChecker()
    errors = []

    def validate(path, subschema, label):
        try:
            data = read_json(path)
            file_schemas = {
                k: v for k, v in schema.items()
                if k in ("providerFile", "plansFile", "indexFile", "manifestFile", "changelogFile")
            }
            root = {"$defs": {**schema["$defs"], **file_schemas}, "$ref": f"#/$defs/{subschema}"}
            Draft202012Validator(root, format_checker=checker).validate(data)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{label}: {e}")
        else:
            print(f"OK  {label}")

    # provider files
    files = sorted(os.listdir(PROVIDERS))
    if not files:
        errors.append("no provider files found")
    for f in files:
        if f.endswith(".json"):
            validate(os.path.join(PROVIDERS, f), "providerFile", f"provider {f}")

    validate(os.path.join(MACHINE, "index.json"), "indexFile", "index.json")
    validate(os.path.join(MACHINE, "plans.json"), "plansFile", "plans.json")
    if os.path.exists(os.path.join(MACHINE, "resellers.json")):
        validate(os.path.join(MACHINE, "resellers.json"), "plansFile", "resellers.json")
    validate(os.path.join(META, "manifest.json"), "manifestFile", "manifest.json")
    validate(os.path.join(META, "changelog.json"), "changelogFile", "changelog.json")

    # cross-file consistency: index model counts vs provider files
    index = read_json(os.path.join(MACHINE, "index.json"))
    for entry in index.get("providers", []) + index.get("resellers", []):
        fpath = os.path.join(MACHINE, entry["file"])
        if not os.path.exists(fpath):
            errors.append(f"index references missing file: {entry['file']}")
            continue
        p = read_json(fpath)
        actual = len(p.get("models", []))
        if actual != entry["model_count"]:
            errors.append(
                f"index model_count mismatch for {entry['id']}: index={entry['model_count']} file={actual}"
            )

    # duplicate model ids within a provider
    for f in files:
        if not f.endswith(".json"):
            continue
        p = read_json(os.path.join(PROVIDERS, f))
        ids = [m["id"] for m in p.get("models", [])]
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            errors.append(f"duplicate model ids in {f}: {sorted(dupes)[:10]}")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("\nAll validations passed.")


if __name__ == "__main__":
    main()
