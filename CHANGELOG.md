# Changelog

## 0.2.0

- CLI discoverability: per-argument help, standard invocations and exit codes in --help,
  plus --version.
- Row-index context in status, score, and reason validation messages.
- HTML how-to-read legend (missing, unexpected, errored with score, unscored,
  score-present coverage, exit codes) with escaped ID lists; report.json bytes unchanged.

## 0.1.1

- Regenerate committed example report hashes from the canonical LF input files.
- Add a regression comparing the full committed JSON snapshot with actual CLI output.
- Runtime behavior and original immutable v0.1.0 release are unchanged.

## 0.1.0

- Strict coverage auditing with explicit population and independent score availability.
- Safe deterministic JSON and escaped HTML reports; synthetic examples and tests.
- GitHub-only wheel/sdist distribution and static executed Pages report.
