# Bounded usefulness exercise

Actor: Codex, AI-assisted. Original synthetic non-client four-ID specimen in
examples/. No external participant, adoption, timed study or independent labeler.

Baseline: inspect the manifest and three rows. case-1 scored; case-2 errored;
case-3 unscored; set subtraction gives missing case-4. One of four expected IDs
has a score. Available-score mean1 does not establish complete coverage. These
expectations were fixed from the declared inputs before implementation.

Actual CLI: expected4/scored1/errored1/unscored1/missing1/score_present1,
coverage0.25, missing case-4, exit1. No unexpected ID or partial errored score in
this specimen; separate tests exercise both. No false alarm against this bounded
task, with no general false-positive rate. Byte hashes: examples/report.json.

Writing a manifest and normalizing producer records is preparation overhead.
One command then produces repeatable counts and missing IDs. For a small file,
conversion may cost more than manual inspection. [Inspect](https://inspect.aisi.org.uk/)
already provides native solver diagnostics and sample views.

This establishes a usable coverage workflow. Speed improvement, broad demand,
production use, model-quality insight and comparative superiority remain unproven.
