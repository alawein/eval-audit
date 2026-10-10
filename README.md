# Eval Audit

Find gaps in evaluation results before interpreting the scores.

![Evaluation coverage](assets/label-purpose.svg)
![Python](assets/label-stack.svg)
![Offline CLI](assets/label-runtime.svg)

Declare the expected IDs and supply JSONL results. Eval Audit separates scored,
errored, unscored, missing, and unexpected records, including errored records
that retain a score.

## Run

Python 3.13+. Download the wheel from this repository's Releases and install it
with `python -m pip install path/to/eval_audit-0.2.0-py3-none-any.whl`.
No runtime dependencies. From a clone:

```sh
uv sync --frozen
uv run eval-audit examples/manifest.json examples/results.jsonl
```

JSON prints to stdout by default, so a first run writes nothing to the repo. Add
`--html report.html` or `--json report.json` for files; reruns over an existing
path need `--force`. `eval-audit --help` shows the manifest and JSONL shapes, the
standard invocations, and exit-code meanings.

The synthetic example exits **1**: four expected IDs, one scored, one errored,
one unscored and one missing. Score-present coverage is 0.25. Exit 0 means a
complete scored population; exit 2 means invalid input or an I/O failure.

## Agent Acceptance demo

Agent Acceptance is a working demo title for synthetic refund case 1042. Audit
the supplied evaluation rows with the same offline engine:

```sh
uv run eval-audit examples/acceptance-manifest.json examples/acceptance-results.jsonl
uv run python scripts/build_demo.py
```

Open `site/acceptance.html` locally. The original example remains at
`site/index.html`, with links between both pages. The refund example declares four
expected IDs: one scored with **0**, one errored retaining **0.9**, one unscored,
and one missing. Two of four IDs have a numeric score, so score-present coverage
is **0.5 (50%)** and the exit code is **1**. Zero is present; an errored record
retaining a number stays errored.

This is score availability, not refund correctness or task quality. The auditor
does not decide whether the supplied refund claim is correct, the completion
observation is fresh, or the agent caused a change. The source text provides
context for original synthetic, AI-assisted, non-client CC0 fixtures.

The page shows expected-record cards, reasons, provenance, and input hashes. It
links to `acceptance-report.json` and byte-for-byte copies of the manifest,
results, and source text. Report hashes cover the manifest and results; a separate
displayed source SHA-256 covers the source bytes. Hashes show consistency, not
authenticity. The report JSON contract remains unchanged.

## Capabilities and limits

Deterministic JSON, readable HTML, input SHA-256 hashes, sorted missing/unexpected
IDs, and errored records retaining a score. The population is supplied, never
guessed. Zero is a present score. Unexpected records do not inflate counts.

No accuracy, quality, means or rankings. It cannot verify the supplied population
or whether a partial score is usable. Native framework diagnostics remain useful.

Troubleshooting: status, score, and reason errors name the JSONL row (for example
`invalid status at record 2`); open that line before editing the file. The HTML
report's how-to-read section explains missing, unexpected, errored with score,
unscored, score-present coverage, and exit codes. [Input contract](docs/contract.md),
[test evidence](docs/evaluation.md), [usefulness exercise](docs/usefulness.md),
[provenance](docs/provenance.md).

## Develop

`just check` runs Ruff, pytest and wheel/sdist builds.
`uv run python scripts/build_demo.py` creates both static executed examples locally.
CLI does not fetch data or call a model. HTML escapes imported text. Existing
outputs require `--force`; outputs cannot alias inputs. Writes are not a multi-file
transaction: a write failure may leave partial output.

MIT code; original CC0 synthetic fixtures. AI-assisted independent implementation.
No client work, production ownership or adoption claim.
