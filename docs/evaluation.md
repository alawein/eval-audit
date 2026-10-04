# Functional evidence

42 local tests passed on Python 3.13 after an initial missing-module failure.
Six status cases pin complete, missing, scored-zero, errored-null, errored-partial
and unscored-null outcomes. Other cases cover unexpected IDs, order invariance,
invalid numbers, duplicate keys/IDs, unknown fields, empty populations, limits,
UTF-8/BOM, U+2028, large integers, 10,000 IDs, hard-link preservation, HTML escaping
and CLI help. New tests cover --help content, row-index errors, the how-to-read legend,
escaping of missing-ID lists, CRLF records, and missing input/output-dir negatives.

One oversized test initially failed in pytest setup: its default case ID exceeded
Windows path limits. Short explicit IDs repaired the harness. No product mismatch
remained. Tests do not establish semantic evaluation quality. Actual released
artifact and hosting checks are recorded in release notes after execution.
