# Input contract v1

Manifest fields exactly: schema_version (integer 1), run_id (nonblank string <= 200),
expected_ids (1..10,000 unique nonblank strings <= 200 each). JSONL record fields
exactly: id (unique nonblank string <= 200), status (scored|errored|unscored), score
(finite number or null), reason (string <= 4,000, possibly empty). Booleans are not
numbers. Scored requires a number; unscored requires null; errored permits either.

Each file: UTF-8 without BOM, <= 5 MiB. Records <= 10,000. Empty results are valid,
blank rows invalid. LF separates rows; final LF optional. CRLF works as JSON
whitespace. U+2028 is content. Duplicate JSON keys and unknown fields fail.

`eval-audit MANIFEST RECORDS [--json PATH] [--html PATH] [--force]` prints JSON
unless --json is supplied. Hashes cover exact input bytes. Expected IDs define
counts. Score coverage includes scored and errored records with a number. Missing
and unscored records stay separate. Output parents must exist; resolved aliases
and existing hard links are rejected. No race-proof filesystem transaction.
