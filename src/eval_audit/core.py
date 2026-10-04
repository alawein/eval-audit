from eval_audit.contract import validate


def audit(manifest: dict, records: list[dict]) -> dict:
    validate(manifest, records)
    expected = set(manifest["expected_ids"])
    indexed = {row["id"]: row for row in records}
    present = [indexed[key] for key in sorted(expected & indexed.keys())]
    missing = sorted(expected - indexed.keys())
    unexpected = sorted(indexed.keys() - expected)
    counts = {"expected": len(expected)}
    counts.update(
        {
            status: sum(row["status"] == status for row in present)
            for status in ("scored", "errored", "unscored")
        }
    )
    counts["missing"] = len(missing)
    counts["score_present"] = sum(row["score"] is not None for row in present)
    return {
        "schema_version": 1,
        "run_id": manifest["run_id"],
        "counts": counts,
        "score_present_coverage": counts["score_present"] / len(expected),
        "missing_ids": missing,
        "unexpected_ids": unexpected,
        "errored_with_score_ids": sorted(
            row["id"] for row in present if row["status"] == "errored" and row["score"] is not None
        ),
        "exit_code": int(bool(missing or unexpected or counts["errored"] or counts["unscored"])),
    }
