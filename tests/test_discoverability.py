import json
import tomllib
from pathlib import Path

import pytest
from test_audit import manifest as make_manifest
from test_audit import row as make_row

from eval_audit.cli import __version__, main
from eval_audit.contract import InputError, validate
from eval_audit.core import audit
from eval_audit.report import render_html


def test_distribution_metadata_preserves_module_and_cli():
    project = tomllib.loads(
        (Path(__file__).parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    )["project"]
    assert project["name"] == "alawein-eval-audit"
    assert project["version"] == "0.3.1"
    assert project["scripts"] == {"eval-audit": "eval_audit.cli:main"}
    assert project["dependencies"] == []


def test_help_documents_invocations_and_exit_codes(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "examples/manifest.json" in out
    assert "exit" in out.lower()
    assert "contract" in out.lower()


def test_status_score_reason_errors_carry_row_index():
    with pytest.raises(InputError) as excinfo:
        validate(make_manifest(), [make_row("unknown")])
    assert "record 1" in str(excinfo.value)
    with pytest.raises(InputError) as excinfo:
        validate(make_manifest(), [make_row("scored", None)])
    assert "record 1" in str(excinfo.value)
    with pytest.raises(InputError) as excinfo:
        validate(make_manifest(), [make_row("unscored", 1)])
    assert "record 1" in str(excinfo.value)


def test_crlf_records_parse():
    import tempfile
    from pathlib import Path

    from eval_audit.contract import load_inputs

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        manifest_path = root / "manifest.json"
        records_path = root / "records.jsonl"
        manifest_path.write_text(json.dumps(make_manifest()), encoding="utf-8")
        records_path.write_bytes((json.dumps(make_row()) + "\r\n").encode())
        _, rows, _ = load_inputs(manifest_path, records_path)
        assert rows[0]["status"] == "scored"


def test_cli_missing_inputs_and_output_dir(tmp_path):
    missing_manifest = tmp_path / "no-manifest.json"
    missing_records = tmp_path / "no-records.jsonl"
    assert main([str(missing_manifest), str(missing_records)]) == 2
    manifest_path = tmp_path / "manifest.json"
    records_path = tmp_path / "records.jsonl"
    manifest_path.write_text(json.dumps(make_manifest()), encoding="utf-8")
    records_path.write_text(json.dumps(make_row()) + "\n", encoding="utf-8")
    target = tmp_path / "no-such-dir" / "out.json"
    assert main([str(manifest_path), str(records_path), "--json", str(target)]) == 2
    assert not target.exists()


def test_report_explains_counts_and_exit_code():
    report = audit(make_manifest(["a", "b"]), [make_row()])
    page = render_html(report)
    assert "How to read" in page
    assert "missing" in page.lower()
    assert "coverage" in page.lower()
    assert "exit" in page.lower()
    assert "<script>" not in page


def test_report_escapes_imported_text():
    report = audit(make_manifest(["a", "<script>"]), [make_row(identifier="a")])
    page = render_html(report)
    assert "<script>" not in page
    assert "&lt;script&gt;" in page


def test_version_flag_prints_carried_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    out = capsys.readouterr().out.strip()
    assert out == f"eval-audit {__version__}"
    assert __version__[0].isdigit()


def test_reason_and_score_errors_carry_row_two():
    overflow = make_row()
    overflow.update({"id": "b", "reason": "x" * 4001})
    with pytest.raises(InputError) as excinfo:
        validate(make_manifest(), [make_row(), overflow])
    assert "record 2" in str(excinfo.value)
    nonfinite = make_row()
    nonfinite.update({"id": "b", "score": float("nan")})
    with pytest.raises(InputError) as excinfo:
        validate(make_manifest(), [make_row(), nonfinite])
    assert "record 2" in str(excinfo.value)


def test_duplicate_record_error_names_row():
    duplicate = {"id": "b", "status": "scored", "score": 1, "reason": ""}
    with pytest.raises(InputError) as excinfo:
        validate(make_manifest(["a", "b"]), [make_row(), duplicate, dict(duplicate)])
    assert "record 3" in str(excinfo.value)


def test_report_escapes_unexpected_and_errored_lists():
    report = audit(
        make_manifest(["a"]),
        [
            make_row(),
            make_row("errored", 0.5, identifier="<b>err</b>"),
            make_row("unscored", None, identifier="<script>"),
        ],
    )
    page = render_html(report)
    assert "<script>" not in page
    assert "&lt;b&gt;err" in page
    assert "&lt;script&gt;" in page
