# Local per-sample adapters

Conversion requires the caller's manifest. Nothing in a source log determines
expected IDs or trials. A source can omit expected cases; auditing the converted
rows reveals these gaps. No files are fetched and no framework package is needed.
All source records are processed or conversion fails. Never pass aggregate metrics
as per-sample results.

`eval-audit convert FORMAT SOURCE --manifest PATH --output PATH [--score-key KEY]
[--score-map MAP.json] [--force]` returns 0 on conversion and 2 on invalid input
or I/O failure. Conversion success does not establish complete coverage; run the
normal audit afterward. JSONL output is sorted by `(id, trial)`.

| Format | Input | Exact mapping |
| --- | --- | --- |
| inspect | JSON object with `samples` array; ZIP `.eval` entries under `samples/` ending `.json` | `id` string or integer becomes string; `epoch` becomes trial, default 1; `scores[KEY].value` becomes score; `error.message` or string error becomes reason |
| lm-evaluation-harness | per-sample JSONL, one task/configuration per file | `doc_id` becomes string ID; literal row key KEY becomes score; optional `error` becomes reason; trial 1 |
| promptfoo | object whose `results` is an array or whose `results.results` is an array | ID is `testIdx:promptIdx`, both nonnegative integers; top-level `score` retained; optional `trial`, default 1; `error` retained as reason |

Source errors, including empty error objects, yield `errored`; otherwise non-null
scores yield `scored`, and absent/null scores yield `unscored`. Failed grading
(`success: false`) is still a delivered numeric score, not an execution error.
Zero remains present. An errored sample retaining a score remains errored.
Inspect missing score keys fail if another score is present, avoiding accidental
selection of the wrong scorer. Samples without any scores become unscored.

Scores must be finite numbers; booleans, arrays and objects fail. Categorical
strings fail unless an explicit `--score-map` JSON object maps them to finite
numbers, for example `{"C":1,"I":0,"P":0.5,"N":0}`. This is a caller-selected
mapping, never an inferred correctness judgment. Unmapped strings fail. Numeric
core validation remains unchanged. Lexically invalid JSON constants fail at the
source level; valid JSON score-type errors name the converted record number.

For Inspect epochs greater than 1, use a trial-enabled manifest. Multiple files
or multiple lm-harness tasks must be converted separately with disjoint explicit
IDs. Promptfoo repeated `(testIdx,promptIdx)` pairs need explicit `trial`; no retry
or provider-order inference is made. Duplicates fail, including duplicate ZIP
member names. This intentionally rejects ambiguous superseded ZIP entries rather
than silently choosing the newest. Archives are never extracted.

Discarded fields: conversations, prompts, responses, tool calls, event timelines,
attachments, model configuration, aggregate metrics, timestamps, token usage,
grading details and source run metadata. Source `error.message` is preserved;
other error fields and traceback are discarded. No arbitrary scorer dictionaries
or arrays are reduced. Run IDs come from the manifest. Full source bytes remain
the caller's provenance owner; converted-file hashes bind the audit's inputs.

Limits: compressed source <=5 MiB; total ZIP expanded bytes <=5 MiB, <=20,000 ZIP
members, <=10,000 sample rows. No remote references, attachment resolution, log
retries, epoch aggregation or aggregate-only reports are supported. Existing
output safety protections apply to manifests, source logs and score maps.

Shapes checked against the official [Inspect log documentation](https://inspect.aisi.org.uk/eval-logs.html),
[Inspect ZIP recorder source](https://github.com/UKGovernmentBEIS/inspect_ai/blob/main/src/inspect_ai/log/_recorders/eval.py),
[lm-harness evaluator](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/evaluator.py),
and [promptfoo output documentation](https://www.promptfoo.dev/docs/configuration/outputs/).
Only synthetic fixtures are vendored in tests. Framework evolution may require a
new adapter version; unsupported structures fail rather than disappearing.
