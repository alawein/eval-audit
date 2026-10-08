# Eval Audit

Find gaps in evaluation results before interpreting the scores.

![Evaluation coverage](assets/label-purpose.svg)
![Python](assets/label-stack.svg)
![Offline CLI](assets/label-runtime.svg)

Declare the expected IDs and supply JSONL results. Eval Audit separates scored,
errored, unscored, missing, and unexpected records, including errored records
that retain a score.

## Run

Python 3.11+. Build the v0.3.0 wheel from this branch with `uv build`, then install it
with `python -m pip install path/to/eval_audit-0.3.0-py3-none-any.whl`.
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

## Capabilities and limits

Deterministic JSON, readable HTML, input SHA-256 hashes, sorted missing/unexpected
IDs, and errored records retaining a score. The population is supplied, never
guessed. Zero is a present score. Unexpected records do not inflate counts.

No accuracy, quality, means or rankings. It cannot verify the supplied population
or whether a partial score is usable. Native framework diagnostics remain useful.

For repeated trials, add `"trials_per_id": 5` to the manifest, or an exact ID-to-count
mapping, and `"trial": 1` to each record. Trial numbers start at 1. Counts include
both ID and trial partitions; IDs are complete only when every planned trial is
delivered. Readiness denominators for pass@k and pass^k require all first k trials
to have `status: scored`. They are counts, never success rates. An errored record
with a numeric score contributes to score availability, but remains errored and
does not qualify for these readiness counts.

Convert local Inspect `.eval`/`.json`, lm-evaluation-harness per-sample JSONL or
promptfoo JSON with an explicit population:

```sh
uv run eval-audit convert inspect log.json --manifest manifest.json --score-key metric --output results.jsonl
uv run eval-audit manifest.json results.jsonl
```

[Adapter mappings and discarded fields](docs/adapters.md) explain supported shapes,
categorical score maps and limitations. [Versioned JSON Schemas](schema/manifest.v1.json)
describe the portable formats. Schema-1 inputs without trials keep their v0.2.0
output shape exactly; schema 2 enables trials and defaults to one trial per ID.

Troubleshooting: status, score, and reason errors name the JSONL row (for example
`invalid status at record 2`); open that line before editing the file. The HTML
report's how-to-read section explains missing, unexpected, errored with score,
unscored, score-present coverage, and exit codes. [Input contract](docs/contract.md),
[test evidence](docs/evaluation.md), [usefulness exercise](docs/usefulness.md),
[provenance](docs/provenance.md).
[Related work and first-PR check history](docs/related-work.md) put these checks
in context; [the public-log pilot](studies/inspect-security-guide/README.md) is a
small recorded-run exercise with its stated limits.

## Develop

`just check` runs Ruff, pytest, type checks, schemas and wheel/sdist builds.
`uv run python scripts/build_demo.py` creates the static executed Pages example.
CLI does not fetch data or call a model. HTML escapes imported text. Existing
outputs require `--force`; outputs cannot alias inputs. Each output is staged in
its destination directory and installed atomically. Writes are not a multi-file
transaction: one complete file can be installed before another fails. A staging
or installation failure preserves that file's previous bytes. This does not
provide race-proof input identity checks or a power-loss durability guarantee.

This is [alawein/eval-audit](https://github.com/alawein/eval-audit), an offline
coverage auditor. It is unrelated to similarly named statistical or human-grading
tools. No registry publication or third-party adoption is claimed.

MIT code; original CC0 synthetic fixtures. AI-assisted independent implementation.
No client work, production ownership or adoption claim.
