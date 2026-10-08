# Release readiness

## Current state, October 8, 2026

v0.3.0 [PR 15](https://github.com/alawein/eval-audit/pull/15) merged at
`b3d116f66840387013848781daa66f3968c9a5d6`. The immutable `v0.3.0` tag and
[GitHub Release](https://github.com/alawein/eval-audit/releases/tag/v0.3.0) exist.
[Registry run](https://github.com/alawein/eval-audit/actions/runs/37799361873)
failed with `invalid-publisher`, because PyPI found no publisher matching the
valid token claims. Separately, its authenticated pending-publisher form rejected
`eval-audit` as too similar to an existing project. Its JSON 404 was not name
acceptance. Local v0.3.0 GitHub assets retain their documented CI-attestation
limitation; preserve their bytes and tag.

The owner authorized the remaining closeout, including registry setup, publication,
merge, tags, release, Pages and non-Dependabot controls. No repeated approval is
needed for that named scope. Preserve feature branches and avoid `--delete-branch`,
`--admin`, force pushes or rewritten tags. Dependabot's entire family is excluded.

Maintenance distribution `alawein-eval-audit` version 0.3.1 is implemented locally.
Repository `eval-audit`, module `eval_audit` and command `eval-audit` are unchanged.
Pending-publisher acceptance and publication have not completed: the authenticated
PyPI session needs owner-entered sensitive-action password confirmation. This is
an access blocker, not a new approval gate. Do not put credentials in logs or use
tokens as a workaround. If the form rejects the default, record its exact cause
before trying the authorized `alawein-evaluation-audit` alternative.

## Maintenance delivery

Register the accepted project's [pending publisher](https://pypi.org/manage/account/publishing/):
GitHub owner `alawein`, repository `eval-audit`, workflow `release.yml`, environment
`pypi`. After reviewed checks and merge, tag the exact main revision `v0.3.1`.
Check that the tag is absent before creating it; never alter `v0.3.0`.

The tag-only release workflow builds once with the locked backend, verifies exact
wheel/sdist metadata and SHA-256, attests them, then retains
`canonical-distributions` for 30 days before registry authentication. SHA256SUMS
and inventory.json are outside dist, so neither can be sent to PyPI as a package.
Publishing and GitHub Release upload consume those exact retained files.
Only release-upload has contents:write. Existing mismatching GitHub assets fail.

For a failed publishing run, rerun failed jobs using its retained canonical
artifact. Preflight checks any existing version's complete inventory and downloads
to confirm exact hashes. Matching existing versions skip publication; changed or
partial versions fail. HTTP 403, other API failures and uncertain effects are not
absence. Reconcile at the destination before any retry. A success must not be
retried blindly. If the canonical artifact expires, stop and prepare a new version
instead of reconstructing old bytes.

After success, the workflow downloads the PyPI distributions and verifies hashes,
GitHub build provenance with exact repository/workflow/source commit/tag and hosted
runner constraints, and PyPI publish provenance. It uploads the identical built
files and checksums, then downloads every GitHub asset to verify bytes. A new
release is complete only after these actual remote checks pass. See
[GitHub verification flags](https://cli.github.com/manual/gh_attestation_verify)
and [PyPI provenance verification](https://docs.pypi.org/attestations/consuming-attestations/).

Update v0.3.0's release description to point to the new distribution after actual
success, retaining the old tag/assets. The manual Pages workflow remains authorized;
verify its run and public page before claiming deployment. Follow
[non-Dependabot security controls](SECURITY_SETTINGS.md).

## Dated prepublication history

Earlier v0.3.0 preparation permitted a draft PR only, and separated merge, tag,
registry, release, Pages and settings gates. Those were the permissions at that
time; the owner's October 8 follow-up superseded them. The original Phase 0 and
prepublication test results remain in [AUDIT_VERIFICATION.md](AUDIT_VERIFICATION.md).
No historical test run is represented as a maintenance validation run.
