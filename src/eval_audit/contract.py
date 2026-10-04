import hashlib
import json
import math
from pathlib import Path


class InputError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InputError(message)


def text(value: object, limit: int, label: str, nonempty: bool = True) -> None:
    require(
        isinstance(value, str) and len(value) <= limit and (not nonempty or bool(value.strip())),
        f"invalid {label}",
    )


def fields(value: object, keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == keys, f"invalid fields: {label}")


def unique_pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value: str) -> None:
    raise InputError(f"nonfinite JSON number: {value}")


def decode(raw: bytes, label: str) -> str:
    require(len(raw) <= 5 * 1024 * 1024, f"{label} exceeds 5 MiB")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{label}: BOM forbidden")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InputError(f"{label}: invalid UTF-8") from exc


def parse(value: str, label: str) -> object:
    try:
        return json.loads(value, object_pairs_hook=unique_pairs, parse_constant=invalid_constant)
    except (json.JSONDecodeError, RecursionError, ValueError) as exc:
        raise InputError(f"{label}: {exc}") from exc


def validate(manifest: dict, records: list[dict]) -> None:
    fields(manifest, {"schema_version", "run_id", "expected_ids"}, "manifest")
    require(
        type(manifest["schema_version"]) is int and manifest["schema_version"] == 1,
        "schema_version must be 1",
    )
    text(manifest["run_id"], 200, "run_id")
    expected = manifest["expected_ids"]
    require(type(expected) is list and 0 < len(expected) <= 10000, "invalid population")
    for identifier in expected:
        text(identifier, 200, "expected ID")
    require(len(set(expected)) == len(expected), "duplicate expected ID")
    require(type(records) is list and len(records) <= 10000, "invalid record count")
    seen = set()
    for index, row in enumerate(records, 1):
        fields(row, {"id", "status", "score", "reason"}, f"record {index}")
        text(row["id"], 200, f"ID at record {index}")
        require(row["id"] not in seen, f"duplicate record ID: {row['id']}")
        seen.add(row["id"])
        require(row["status"] in ("scored", "errored", "unscored"), "invalid status")
        text(row["reason"], 4000, "reason", nonempty=False)
        score = row["score"]
        require(
            score is None or type(score) is int or (type(score) is float and math.isfinite(score)),
            "score must be finite or null",
        )
        require(row["status"] != "scored" or score is not None, "scored needs score")
        require(row["status"] != "unscored" or score is None, "unscored needs null")


def load_inputs(manifest_path: Path, records_path: Path) -> tuple[dict, list[dict], dict]:
    def bounded_read(path: Path) -> bytes:
        with path.open("rb") as stream:
            raw = stream.read(5 * 1024 * 1024 + 1)
        require(len(raw) <= 5 * 1024 * 1024, f"{path.name}: exceeds 5 MiB")
        return raw

    raw_manifest = bounded_read(manifest_path)
    raw_records = bounded_read(records_path)
    manifest = parse(decode(raw_manifest, "manifest"), "manifest")
    decoded = decode(raw_records, "records")
    lines = decoded.split("\n") if decoded else []
    if decoded.endswith("\n"):
        lines.pop()
    require(len(lines) <= 10000, "record count exceeds 10000")
    rows = []
    for index, line in enumerate(lines, 1):
        require(bool(line.strip()), f"blank JSONL row {index}")
        rows.append(parse(line, f"record {index}"))
    validate(manifest, rows)
    hashes = {
        "manifest_sha256": hashlib.sha256(raw_manifest).hexdigest(),
        "records_sha256": hashlib.sha256(raw_records).hexdigest(),
    }
    return manifest, rows, hashes
