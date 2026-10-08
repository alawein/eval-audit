# Shared local output helpers

`src/eval_audit/output.py` intentionally duplicates the stdlib helpers in
`alawein/outcome-check`, `src/outcome_check/output.py`: `same_location`,
`validate_outputs`, and `atomic_write`. Keep these three functions identical.
The v0.3.0 changes were synchronized between both maintainers and tested in both
repositories. No shared runtime package or runtime dependency is introduced.

The output safety contract is per-file atomic installation: same-directory
temporary file, full write/flush/fsync, `os.replace` when forced, `os.link` for
exclusive creation otherwise, then stage cleanup. Validation rejects resolved
aliases and existing hard links before staging. This is not a multi-output
transaction, race-proof input validation, or a power-loss durability guarantee.
