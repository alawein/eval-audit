# Recorded Inspect run pilot

This is an offline coverage re-audit of a recorded upstream GPT-4o-mini run,
not a newly generated dataset or scorer run. The archived task is Inspect's
small security-guide example. It is useful as a reproducible adapter smoke
study, not evidence about benchmark-wide failure rates.

Source: [Inspect log at commit 4acfd207](https://github.com/UKGovernmentBEIS/inspect_ai/blob/4acfd207ecca8e1c3b754a147c191f2f0f21ba71/tests/analysis/test_logs/2025-05-12T20-28-26-04-00_security-guide.json).
Upstream code and archived log are distributed in the MIT-licensed Inspect
repository. Recorded evaluation date: May 12, 2025. Downloaded October 8, 2026.
The log has model messages, token usage, timings, and grader results. None of
those model calls are performed by this study. The third-party log is excluded
from Git; only provenance, the study script, and aggregate results are committed.

```powershell
New-Item -ItemType Directory studies/data -Force
curl.exe -L --fail https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/4acfd207ecca8e1c3b754a147c191f2f0f21ba71/tests/analysis/test_logs/2025-05-12T20-28-26-04-00_security-guide.json -o studies/data/security-guide.json
Get-FileHash studies/data/security-guide.json -Algorithm SHA256
uv run python studies/inspect-security-guide/run.py studies/data/security-guide.json --output studies/inspect-security-guide/results.json
```

SHA-256: `44f6203d88252de0c33f76c948ad7c537b412cff628c704e9a5449ffba9d5a34`.
The script refuses different bytes, uses an explicit manifest `[1,2,3]` from
the recorded header's selected IDs, and supplies the scorer-specific map
`C=1`. It does not infer expected coverage from delivered samples.

The full dataset contains 16 questions; the run selected three with `limit=3`.
Counting the other 13 as missing would be an incorrect denominator. This pilot
finds three scored records, zero missing, zero errored, zero unscored, and a
headline denominator shift of zero (3 to 3). Recorded headline accuracy is 1.0;
this tool audits its availability denominator and does not validate that score.
See [machine-readable results](results.json).

An initial search also located public Hugging Face lm-evaluation-harness logs,
but anonymous downloads returned HTTP 401. The reachable upstream Inspect log
was used instead. No credential was created or supplied.
