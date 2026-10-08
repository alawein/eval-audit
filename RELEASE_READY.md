# v0.3.0 release readiness

Prepared locally, not released. This branch permits one draft PR against `main`.
Merging, tags, GitHub Releases, package publication, Pages deployment, settings,
and secrets are separate owner gates. No step below was executed in this run.

## Merge gate

After explicit merge authorization, mark the draft ready in the PR UI, review
the exact current head and checks, then use the PR number from this branch:

```powershell
gh pr ready --repo alawein/eval-audit 15
gh pr checks --repo alawein/eval-audit 15
gh pr merge --repo alawein/eval-audit 15 --squash --match-head-commit <APPROVED_HEAD_SHA>
```

Do not use `--delete-branch` or `--admin`. Passing checks are not merge permission.
Pages was made manual-only so a separately approved merge does not deploy.

## Tag and package publication gates

`release.yml` triggers only on a pushed `v*` tag, checks that the tagged commit
is an ancestor of `origin/main`, and compares the tag to the package version.
It publishes automatically through a configured trusted publisher. Therefore
**pushing the tag crosses both the tag gate and the package publication gate**.
The workflow uses full action commit SHAs, OIDC, and build attestations.

Configure the trusted publisher only after the owner authorizes registry setup.
The workflow filename is `release.yml`, owner `alawein`, repository `eval-audit`,
environment `pypi`. No secret is needed by the workflow.

After merge, registry configuration, and explicit tag plus publish approval:

```powershell
git fetch origin main
git tag -a v0.3.0 origin/main -m "chore(release): v0.3.0"
git push origin refs/tags/v0.3.0
gh run list --repo alawein/eval-audit --workflow release.yml --limit 1
```

Recheck the exact main revision and the absence of an existing tag before tagging.
Never overwrite a tag. Inspect the finished publishing run and download/check
the registry artifact before claiming that publication succeeded.

For PyPI, visit [pending publishers](https://pypi.org/manage/account/publishing/)
and Add a new pending publisher, choose GitHub, project `eval-audit`, owner `alawein`,
repository `eval-audit`, workflow `release.yml`, environment `pypi`.
[PyPI's publishing instructions](https://docs.pypi.org/trusted-publishers/using-a-publisher/)
support first publication through a pending publisher. Attestations are enabled
in the PyPA publishing action. Builds and `twine check` are local preparation.

`eval-audit` returned HTTP 404 from PyPI's project JSON endpoint on October 8, 2026.
It was available at that lookup, not reserved. Recheck before registry setup.

## GitHub Release gate

Only after explicit release authorization and verified package publication:

```powershell
gh release create v0.3.0 --repo alawein/eval-audit --verify-tag --title "eval-audit v0.3.0" --notes-file RELEASE_NOTES.md dist/*
```

Use the files built from the approved tagged revision. Check uploaded artifact
hashes after downloading them. [Release notes](RELEASE_NOTES.md) are prepared
from the changelog; add the actual published artifact checks after the release.

## Pages deployment gate

The Pages workflow is manual-only. After explicit Pages authorization:

```powershell
gh workflow run pages.yml --repo alawein/eval-audit --ref main
gh run list --repo alawein/eval-audit --workflow pages.yml --limit 1
```

The existing `github-pages` environment and Pages source must be configured by
the owner if absent. Inspect the run and <https://alawein.github.io/eval-audit/> before
claiming deployment. Changing Pages settings is a separate settings gate.

## Security settings gate

Follow [SECURITY_SETTINGS.md](SECURITY_SETTINGS.md) at
<https://github.com/alawein/eval-audit/settings/security_analysis>. Enable dependency
graph, Dependabot alerts, and Dependabot security updates. Add version-update
configuration through a separately authorized PR. No setting was changed here.
