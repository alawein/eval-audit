import argparse
import sys
from pathlib import Path

from eval_audit.contract import InputError, load_inputs, require
from eval_audit.core import audit
from eval_audit.report import render_html, render_json

try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _package_version

    __version__ = _package_version("eval-audit")
except PackageNotFoundError:
    __version__ = "0.2.0"


def same_location(left: Path, right: Path) -> bool:
    if left.resolve() == right.resolve():
        return True
    return left.exists() and right.exists() and left.samefile(right)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit evaluation result coverage.",
        epilog=(
            "manifest shape: schema_version 1 with run_id and expected_ids; "
            "records are JSONL rows with id, status, score, reason; "
            "see docs/contract.md. "
            "example: eval-audit examples/manifest.json examples/results.jsonl. "
            "exit 0 complete scored population; exit 1 work remains; "
            "exit 2 invalid input or I/O."
        ),
    )
    parser.add_argument("manifest", type=Path, help="manifest JSON file")
    parser.add_argument("records", type=Path, help="records JSONL file")
    parser.add_argument("--json", type=Path, help="write the JSON report to PATH")
    parser.add_argument("--html", type=Path, help="write the HTML report to PATH")
    parser.add_argument("--force", action="store_true", help="overwrite existing output files")
    parser.add_argument("--version", action="version", version=f"eval-audit {__version__}")
    args = parser.parse_args(argv)
    try:
        manifest, records, hashes = load_inputs(args.manifest, args.records)
        report = audit(manifest, records) | {"inputs": hashes}
        targets = [(args.json, render_json(report)), (args.html, render_html(report))]
        outputs = [path for path, content in targets if path is not None]
        inputs = [args.manifest, args.records]
        for index, path in enumerate(outputs):
            require(
                not any(same_location(path, prior) for prior in outputs[:index]),
                "output paths must differ",
            )
            require(
                not any(same_location(path, source) for source in inputs),
                "output cannot replace input",
            )
        for path, _content in targets:
            if path is not None:
                require(args.force or not path.exists(), f"output exists: {path}")
                require(path.parent.is_dir(), f"missing output directory: {path.parent}")
        for path, content in targets:
            if path is not None:
                with path.open(
                    "w" if args.force else "x", encoding="utf-8", newline="\n"
                ) as stream:
                    stream.write(content)
        if args.json is None:
            sys.stdout.write(render_json(report))
        return report["exit_code"]
    except (InputError, OSError, OverflowError, RecursionError) as exc:
        print(f"eval-audit: {exc}", file=sys.stderr)
        return 2
