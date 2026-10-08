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

## Dated v0.3.0 release coordination decisions

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

## PyPI first-publication finding (2026-10-08)

The unauthenticated project JSON endpoint returned 404 for `eval-audit`, but this
did not prove that PyPI would accept the name. The authenticated pending-publisher
form rejected it with "This project name is too similar to an existing project."
The planned distribution name is therefore blocked even though no package exists
at that exact JSON endpoint. No package was published under another name.

Historical proposal: `alawein-eval-audit` as the distribution-name alternative, subject to
PyPI's name checks and explicit owner selection. Keep the GitHub repository,
`eval_audit` import package, and `eval-audit` command unchanged. A renamed
distribution needs updated metadata, lockfile, docs, and a release version/tag
decision before publication; do not silently reinterpret the approved v0.3.0 tag.

## Authorized maintenance closeout (2026-10-08)

The owner's follow-up authorizes the reversible default `alawein-eval-audit`
distribution and maintenance version 0.3.1, preserving the repository, import,
CLI and schema/report contracts. Authenticated pending-publisher acceptance is
still unverified: the coordinator encountered an expired sensitive-action
password confirmation and prepared the owner-entry handoff. HTTP 404 is not an
acceptance check. If rejected, use the authorized `alawein-evaluation-audit`
alternative only after recording the actual form result. No new credential is
created as a workaround.

v0.3.0 [PR 15](https://github.com/alawein/eval-audit/pull/15) merged at
`b3d116f66840387013848781daa66f3968c9a5d6`; its immutable tag and
[GitHub Release](https://github.com/alawein/eval-audit/releases/tag/v0.3.0) are
published. [Publishing run](https://github.com/alawein/eval-audit/actions/runs/37799361873)
failed with PyPI `invalid-publisher`: no publisher matched the valid token's
claims. This is distinct from the separately observed name rejection. v0.3.1
publication is not yet attempted. Preserve old tags, feature branches and assets.

The release pipeline has separate build, publish and release-upload jobs. Locked
Hatchling 1.32.4 and pypi-attestations 0.0.30 are development tools only. A retained
canonical artifact is uploaded before registry authentication; retry failed jobs
from that run instead of rebuilding or blindly re-uploading an existing version.
An existing registry version is accepted only with an exact complete inventory
and verified downloaded hashes. Existing differing release assets fail closed.
Checksums live outside dist. Build verification binds repository, workflow,
source commit, tag and hosted runner; registry publish provenance is verified
with PyPI's client. These workflow checks are implemented, not yet executed for
a new published maintenance release.

The larger real Inspect archive has ten explicitly selected trials, all delivered
and all unscored. It is a useful expanded example, not representative benchmark
failure-rate evidence. No scores, errors or headline metric were manufactured.
The original pilot remains intact. Both packages retain duplicated output helpers
and mirrored synthetic vectors rather than introducing a shared dependency.

Dependabot's entire family remains excluded. Existing report-only pip-audit,
full-SHA actions, protected reviews, OIDC and artifact verification provide the
non-Dependabot controls within this scope.
