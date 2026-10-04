from pathlib import Path

from eval_audit.contract import load_inputs
from eval_audit.core import audit
from eval_audit.report import render_html, render_json


def main() -> None:
    manifest, rows, hashes = load_inputs(
        Path("examples/manifest.json"), Path("examples/results.jsonl")
    )
    report = audit(manifest, rows) | {
        "inputs": hashes,
        "provenance": "Synthetic, AI-assisted, non-client",
    }
    target = Path("site")
    target.mkdir(exist_ok=True)
    (target / "index.html").write_text(render_html(report), encoding="utf-8")
    (target / "report.json").write_text(render_json(report), encoding="utf-8")


if __name__ == "__main__":
    main()
