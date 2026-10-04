# Eval audit

Find missing evaluation records before interpreting scores. Declare the expected
IDs and supply JSONL results. Eval audit separates scored, errored, unscored,
missing and unexpected records, including errored records that retain a score.

## Run

Python 3.13+. Download the wheel from this repository's Releases and install it
with `python -m pip install path/to/eval_audit-0.1.0-py3-none-any.whl`.
No runtime dependencies. From a clone:

```sh
uv sync --frozen
uv run eval-audit examples/manifest.json examples/results.jsonl --html report.html
```

The synthetic example exits **1**: four expected IDs, one scored, one errored,
one unscored and one missing. Score-present coverage is 0.25. Exit 0 means a
complete scored population; exit 2 means invalid input or an I/O failure.

## Capabilities and limits

Deterministic JSON, readable HTML, input SHA-256 hashes, sorted missing/unexpected
IDs, and errored records retaining a score. The population is supplied, never
guessed. Zero is a present score. Unexpected records do not inflate counts.

No accuracy, quality, means or rankings. It cannot verify the supplied population
or whether a partial score is usable. Native framework diagnostics remain useful.

[Input contract](docs/contract.md), [test evidence](docs/evaluation.md),
[usefulness exercise](docs/usefulness.md), [provenance](docs/provenance.md).

## Develop

`just check` runs Ruff, pytest and wheel/sdist builds.
`uv run python scripts/build_demo.py` creates the static executed Pages example.
CLI does not fetch data or call a model. HTML escapes imported text. Existing
outputs require `--force`; outputs cannot alias inputs. Writes are not a multi-file
transaction: a write failure may leave partial output.

MIT code; original CC0 synthetic fixtures. AI-assisted independent implementation.
No client work, production ownership or adoption claim.
