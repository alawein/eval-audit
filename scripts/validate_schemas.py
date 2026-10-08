"""Development-only validation of published schemas and example bytes."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from eval_audit.contract import load_inputs
from eval_audit.core import audit


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    validators = {}
    for name in ("manifest", "result-record", "report"):
        schema = json.loads((root / "schema" / f"{name}.v1.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(schema)
    for directory in (root / "examples", root / "examples" / "trials"):
        manifest, rows, hashes = load_inputs(
            directory / "manifest.json", directory / "results.jsonl"
        )
        validators["manifest"].validate(manifest)
        for row in rows:
            validators["result-record"].validate(row)
        validators["report"].validate(audit(manifest, rows) | {"inputs": hashes})
        validators["report"].validate(json.loads((directory / "report.json").read_text()))
    print("PASS: Draft 2020-12 schemas; legacy and trial examples")


if __name__ == "__main__":
    main()
