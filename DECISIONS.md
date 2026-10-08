# v0.3.0 decisions

- Legacy schema-1 input without `trials_per_id` returns the identical schema-1
  report and still rejects duplicate IDs. Extended input accepts schema 1 or 2;
  schema 2 enables trial mode with default one trial. Extended reports use 2.
- Trials are one-based positive integers. `trials_per_id` is a positive integer
  or an exact expected-ID mapping. Total planned trials and delivered rows are
  capped at 10,000. In trial mode absent row trial means trial 1.
- ID status precedence is missing, errored, unscored, scored. Thus mixed trial
  statuses have exactly one ID category and the partition invariant holds.
  Complete means all expected trials delivered, independent of scoring.
- For each k, eligible IDs must plan at least k trials. Pass@k and pass^k
  denominator readiness counts IDs with trials 1..k all in scored status.
  They have the same readiness denominator; no correctness or success rates
  are computed. Errored-with-score contributes to availability only.
- Adapters require an explicit caller manifest and named score key for Inspect
  and lm-evaluation-harness. Framework fields are never used to infer expected
  population. Conversion validates every source row and canonical output.
- Atomic output guarantees apply per file. Several outputs are not one
  transaction. Existing aliases and hard links are rejected before staging.
- Order invariance applies to audit counts and report bodies. CLI input hashes
  bind exact file bytes, so reordering JSONL bytes correctly changes the input
  digest even when the audit body is identical. Source bytes are never normalized
  solely to equalize hashes.

## Release coordination decisions

Hosted link checks returned 404 only for the repository's maintainer-only security
settings URL. Keep its exact click path, exclude only that anchored URL from
anonymous lychee probes, and continue checking all public research/document links.
Read-only API checks separately established the disabled alerts/update settings.
No setting or credential was changed to make the check pass.

Pages deployment is manual-only so approving a merge does not also approve
hosting. A release tag starts trusted package publication, so the tag requires
both tag and registry publication authorization. npm first-publication bootstrap,
if needed, is a separate owner-approved publication using existing access; this
run does not create secrets or bypass registry setup.
