# Audit verification

## Phase 0, October 8, 2026

Source: `compass_artifact_wf-8f32e147-9bf3-5208-ba05-acfbbd390eae_text_markdown.md`,
full supplied audit read locally. Baseline HEAD: `06b6d1eebe01455b08277a2caace54aa2417af28`.
Branch: `feat/v0.3.0-hardening`; clean before work.

`uv sync --frozen` succeeded. Python used by baseline: 3.13.9; system Python:
3.14.7; Node: 22.23.2. pytest: **46 passed**, no skips, failures or deselections.
Ruff check passed; Ruff format: 21 files already formatted. Wheel and sdist built.
Lock SHA-256: `c2a1c04338dfb918b3562e2a82ac6d60d047cdfa4d9a025c30b8c85298117117`.
Runtime dependency list is empty; development lock contains pytest and Ruff.

| Audit assertion | Finding at baseline | Evidence |
| --- | --- | --- |
| Offline runtime not verifiable | Confirmed offline statically | `core.py:1`, `contract.py:1-4`, `cli.py:1-7`: only stdlib/local imports; no network, model, subprocess or executor calls anywhere in runtime |
| Explicit denominator unclear | Confirmed correct | `core.py:11,24`: supplied expected-ID count is denominator; unexpected IDs excluded by expected intersection at line 8 |
| Error scores' numerator unclear | Refuted as code defect; documentation partially clear | `core.py:19,27-28`: every expected non-null score counts, including errored records; separate list preserved; contract states this explicitly |
| NaN/infinity/booleans unknown | Refuted as code defect | `contract.py:78-81`: bool rejected by exact type checks; nonfinite float rejected; JSON constants rejected at lines 37-38; numeric overflow `1e999` rejected after parsing; errors include row |
| Repeated trials unsupported | Confirmed | `contract.py:70-73` requires exact legacy fields and unique ID |
| No native adapters | Confirmed | Only canonical JSON/JSONL reader in `contract.py:91`; CLI exposes no conversion |
| Python floor 3.13 unnecessarily restrictive | Confirmed floor; no inspected runtime syntax needs 3.13 | `pyproject.toml` requires >=3.13; lowering and actual matrix tests planned |
| Writes may truncate existing output | Confirmed | `cli.py:64-68` writes target directly |
| No schemas/property tests | Confirmed | No schema directory or Hypothesis dev dependency/tests |
| Historical counts disagree | Current count resolved | 46 collected and passed at specified baseline; historical PR/check evidence owned by root |
| Synthetic-only empirical evidence | Confirmed baseline | examples and usefulness docs synthetic; public study owned by root |
| Name collisions | Partial | README lacks disambiguation; externally verified registry/name evidence owned by root |
| Registry/security/first-PR checks | Partial, remote verification pending | Root owns checks, settings and release-readiness documentation |

No source changes were made before these checks. Review claims about other two
repositories are outside this checkout; their assigned agents own verification.

## v0.3.0 local verification

The final suite collects **93 tests** (baseline 46), all passing on Python
**3.11.13, 3.12.10 and 3.13.9**. Two Hypothesis properties each exercise 100
deterministic generated cases. Ruff check/format, mypy and Pyright pass. Draft
2020-12 schema definitions and legacy/trial examples validate. Both wheel and
sdist build through `uv build` and `python -m build`; Twine metadata checks pass.
Both artifacts install in isolated environments and pass the synthetic CLI smoke.
`uv sync --frozen` succeeds after lowering the floor. Runtime dependencies remain
empty. Final lock SHA-256:
`752b4947bd88982d98b56a7a837186aa013d1537439646d58cb259f4808f1de8`.

| Addressed finding | Current code evidence |
| --- | --- |
| Offline core and adapters | `core.py:1`, `contract.py:1-5`, `cli.py:1-14`, `adapters.py:3-6`, `output.py:3-5`: stdlib/local imports; inspected runtime has no network/model/subprocess/executor calls |
| Explicit denominators and legacy compatibility | `core.py:26,97,99`: supplied ID/trial populations; committed legacy JSON unchanged and full snapshot test passes |
| Errored numeric availability | `core.py:21,54,71`: availability counts numeric error scores; `core.py:74-90` separately excludes errors from all-k-scored readiness |
| Numeric and duplicate validation | `contract.py:113,121`: exact pair duplicate and finite exact numeric types, row-numbered; parser rejects nonfinite lexical constants at line 37 |
| Repeated trials | `contract.py:56-75`, `core.py:35-126`: explicit plans, expected/delivered/duplicate/unexpected counts, missing pairs, mixed statuses and readiness counts |
| Adapters | `adapters.py`: narrow explicit mappings; synthetic tests and caller-selected categorical mappings; docs/adapters.md lists discarded fields and limits |
| Output preservation | `output.py:26-48`: same-directory staging and atomic installation; injected stage-write/replace/link race failures preserve target bytes |
| Shared helper consistency | Both output.py files have SHA-256 `97a0787863525f5fc814e838f557940a226e7c3a31ea6f0b80fd31d038006c31`; SHARED_CODE.md names the three mirrored functions |

Remaining scope boundaries: scores/populations are supplied evidence, no rates or
accuracy inferred. Several file outputs are not one transaction. Archive retries,
arbitrary score objects and aggregate-only reports intentionally fail rather than
being silently normalized. Root owns remote checks/security/release readiness and
the separate three-record public Inspect pilot; its result is not adoption.

Fresh committed-clone verification is pending the product commit below.
