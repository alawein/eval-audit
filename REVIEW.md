# Review guidance

Report concrete defects introduced by the changed lines, with affected paths,
the triggering input and the resulting incorrect behavior. Put findings first,
ordered by impact; keep the summary short. If no actionable defect is found,
say so without inventing tests or claiming execution you did not perform.

Preserve these invariants: explicit caller-supplied planned denominators;
errored-with-score availability never treated as scored readiness; schema-1
legacy bytes and schema behavior unchanged; new semantics versioned and migrated;
deterministic finite JSON and escaped HTML; offline core with no model/network
calls; zero default runtime dependencies; aliases and atomic output errors fail
closed. Atomicity is per file, not a multi-output transaction or crash durability.

Release review checks identical retained build, attestation, registry and GitHub
asset bytes; metadata/version/tag consistency; retries reconciled before writes;
full-SHA actions; and exact source/workflow/tag provenance. Distinguish implemented
checks from actual published results. Preserve existing release tags/assets and
feature branches. Dependabot's entire family is outside this authorized scope.
