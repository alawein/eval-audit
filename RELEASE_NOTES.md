# eval-audit v0.3.0

Release candidate. Publication is gated.

## 0.3.0 (unreleased)

- Add explicit global/per-ID trial plans, trial identities, missing/unexpected
  trial reports, ID completeness and pass@k/pass^k readiness denominators.
- Preserve v0.2.0 single-trial inputs and schema-1 report bytes; document mixed
  status precedence and errored-with-score availability rules.
- Convert local Inspect JSON/.eval, lm-evaluation-harness per-sample JSONL and
  promptfoo JSON with explicit manifests and optional categorical score maps.
- Publish Draft 2020-12 schemas and validate legacy/trial examples; add Hypothesis
  partitions/order checks, negative adapter tests, and mypy/Pyright checks.
- Lower Python floor to 3.11; use per-file atomic exports preserving old bytes
  after staging/install failure and retain alias/hard-link protections.

See [AUDIT_VERIFICATION.md](AUDIT_VERIFICATION.md) for executed checks and limitations,
and [RELEASE_READY.md](RELEASE_READY.md) for gated publication commands.
