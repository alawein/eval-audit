# Ten-sample archived Inspect coverage study

This offline study uses a real recorded upstream run, not a new model or scorer
execution. It expands the retained [three-sample pilot](../inspect-security-guide/README.md)
with a ten-sample archive that actually contains unscored records. It is a bounded
example study, not a representative estimate of harness failure rates.

## Source and planned population

[Pinned archive](https://github.com/UKGovernmentBEIS/inspect_ai/blob/4acfd207ecca8e1c3b754a147c191f2f0f21ba71/tests/scorer/logs/2025-02-11T15-17-00-05-00_popularity_dPiJifoWeEQBrfWsAopzWr.eval)
is distributed in Inspect's MIT-licensed repository. Run date: February 11, 2025.
Downloaded October 8, 2026. Length: 19,561 bytes. SHA-256:
`6631813cb3cc25908d760d36677925a0e5753d06602c7d97385a4f448bafd9a1`.
Third-party log bytes remain outside Git in ignored `studies/data/`.

The header independently declares dataset size 100, selected sample IDs 1 through
10, `limit=10`, and `results.total_samples=10`. The supplied manifest explicitly
plans those ten IDs with one trial each. The other 90 dataset entries are excluded
by upstream selection and are not missing records. No IDs are inferred from the
delivered sample bodies. Score mapping names `match` and declares `C=1`, `I=0`;
all ten archived score dictionaries are empty, so that map is never applied.
Model messages, targets, events, usage, timings, metadata and native aggregate
fields are deliberately discarded by the narrow adapter. No scores are inferred
from model responses or targets. `results.scores` is empty; no upstream headline
denominator or accuracy is asserted.

## Result

[Machine-readable results](results.json): expected 10, delivered 10, scored 0,
errored 0, unscored 10, missing 0, duplicate 0, unexpected 0. All ten IDs are
delivery-complete, while score availability is zero. Planned minus delivered is
zero; planned minus score-available is ten. For the only declared k, k=1,
readiness is 0 of 10 IDs. These are availability counts, not pass@k/pass^k rates.
An errored record retaining a score would remain errored; synthetic adapter tests
cover that rule, but this source has no errors and none were manufactured.

The script checks exact bytes and the header, repeats the audit, permutes the
source sample order and reconverts it. Counts and report bodies must match; the
permuted source byte hash correctly differs. Epochs, missing requested keys,
categorical scores, partial errors and corrupt archives have separate synthetic
negative tests. No adapter mapping defect was reproduced in this archive.

## Reproduce offline

Download the pinned URL above once to `studies/data/popularity.eval`, then:

```sh
uv run python studies/harness-coverage/run.py studies/data/popularity.eval --output studies/harness-coverage/results.json
```

The study script itself never fetches data or calls a model. An upstream search
inspected Inspect's analysis/scorer fixtures: browser selected one sample,
popularity analysis selected three, MMLU choices selected one, and this archived
scorer fixture selected ten. Prior Hugging Face harness downloads returned 401
as recorded in the historical pilot. No credential bypass was used.
