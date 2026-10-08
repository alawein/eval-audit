import json
import zipfile

import pytest
from test_audit import manifest

from eval_audit.adapters import convert
from eval_audit.cli import main
from eval_audit.contract import InputError


def write(tmp_path, value):
    source = tmp_path / "source.json"
    source.write_text(json.dumps(value), encoding="utf-8")
    return source


def test_inspect_epochs_error_and_partial_score(tmp_path):
    samples = [
        {"id": "a", "epoch": 1, "scores": {"metric": {"value": 0}}},
        {
            "id": "a",
            "epoch": 2,
            "error": {"message": "failed"},
            "scores": {"metric": {"value": 0.5}},
        },
    ]
    population = manifest() | {"schema_version": 2, "trials_per_id": 2}
    source = write(tmp_path, {"samples": samples, "eval": {"dataset": {"samples": 999}}})
    rows = convert("inspect", population, source, "metric")
    assert [(r["trial"], r["status"], r["score"]) for r in rows] == [
        (1, "scored", 0),
        (2, "errored", 0.5),
    ]
    archive = tmp_path / "log.eval"
    with zipfile.ZipFile(archive, "w") as stream:
        stream.writestr("header.json", "{}")
        for index, sample in enumerate(samples):
            stream.writestr(f"samples/{index}.json", json.dumps(sample))
    assert convert("inspect", population, archive, "metric") == rows


def test_lm_harness_jsonl_metric_and_missing_score(tmp_path):
    source = tmp_path / "samples.jsonl"
    source.write_text('{"doc_id":0,"acc,none":0}\n{"doc_id":1}\n', encoding="utf-8")
    rows = convert("lm-evaluation-harness", manifest(["0", "1"]), source, "acc,none")
    assert rows == [
        {"id": "0", "status": "scored", "score": 0, "reason": ""},
        {"id": "1", "status": "unscored", "score": None, "reason": ""},
    ]


def test_promptfoo_test_prompt_pair_is_explicit_id(tmp_path):
    source = write(
        tmp_path,
        {
            "results": {
                "results": [
                    {"testIdx": 0, "promptIdx": 1, "success": False, "score": 0},
                    {"testIdx": 1, "promptIdx": 1, "error": "provider failed", "score": 0.2},
                ]
            }
        },
    )
    rows = convert("promptfoo", manifest(["0:1", "1:1"]), source)
    assert rows[0]["status"] == "scored"
    assert rows[1]["status"] == "errored"
    assert rows[1]["score"] == 0.2


@pytest.mark.parametrize("bad", [True, float("nan"), float("inf"), "C", {"metric": 1}])
def test_inspect_rejects_unsupported_score_without_silent_drop(tmp_path, bad):
    source = write(tmp_path, {"samples": [{"id": "a", "scores": {"metric": {"value": bad}}}]})
    with pytest.raises(InputError, match="record 1|source: nonfinite"):
        convert("inspect", manifest(), source, "metric")


def test_inspect_missing_requested_key_errors(tmp_path):
    source = write(tmp_path, {"samples": [{"id": "a", "scores": {"other": {"value": 1}}}]})
    with pytest.raises(InputError, match="score key"):
        convert("inspect", manifest(), source, "metric")


def test_conversion_cli_preserves_source_and_explicit_population(tmp_path):
    source = write(tmp_path, {"samples": [{"id": "a", "scores": {"metric": {"value": 1}}}]})
    population = tmp_path / "manifest.json"
    population.write_text(json.dumps(manifest(["a", "missing"])), encoding="utf-8")
    out = tmp_path / "canonical.jsonl"
    assert (
        main(
            [
                "convert",
                "inspect",
                str(source),
                "--manifest",
                str(population),
                "--score-key",
                "metric",
                "--output",
                str(out),
            ]
        )
        == 0
    )
    assert len(out.read_text().splitlines()) == 1
    before = source.read_bytes()
    assert (
        main(
            [
                "convert",
                "inspect",
                str(source),
                "--manifest",
                str(population),
                "--score-key",
                "metric",
                "--output",
                str(source),
                "--force",
            ]
        )
        == 2
    )
    assert source.read_bytes() == before


def test_duplicate_zip_sample_names_rejected(tmp_path):
    source = tmp_path / "log.eval"
    with zipfile.ZipFile(source, "w") as stream:
        stream.writestr("samples/a.json", '{"id":"a"}')
        with pytest.warns(UserWarning):
            stream.writestr("samples/a.json", '{"id":"b"}')
    with pytest.raises(InputError, match="duplicate"):
        convert("inspect", manifest(), source, "metric")


def test_explicit_categorical_mapping_is_required(tmp_path):
    source = write(tmp_path, {"samples": [{"id": "a", "scores": {"metric": {"value": "C"}}}]})
    with pytest.raises(InputError):
        convert("inspect", manifest(), source, "metric")
    assert convert("inspect", manifest(), source, "metric", {"C": 1})[0]["score"] == 1
    with pytest.raises(InputError, match="record 1"):
        convert("inspect", manifest(), source, "metric", {"I": 0})
    with pytest.raises(InputError):
        convert("inspect", manifest(), source, "metric", {"C": True})
