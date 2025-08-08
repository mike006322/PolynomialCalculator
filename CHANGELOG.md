# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [0.2.1] - 2025-08-08
### Changed
- Lint cleanup: Resolved all Ruff errors (E402/E721/E741/F841) across CLI, parser, ideal, demo, and algebra modules.
- Enforced blocking lint in CI; Ruff/Black failures now fail the workflow.
- Minor refactors for clarity (rename ambiguous variables, isinstance usage).

### Fixed
- Import order and residual indentation issues in tests; unit tests all pass.

## [0.2.0] - 2025-??-??
### Added
- Structured JSON output for CLI subcommands: `solve`, `solve-system`, and `groebner` with consistent error payloads and exit codes.
- Logging improvements with `--verbose`/`--quiet` and `POLYCALC_DEBUG`.
- GitHub Actions CI across OS/Python versions; non-blocking lint initially.

### Changed
- Performance improvement in `Polynomial.__pow__` (exponentiation by squaring).
- Packaging/versioning tweaks; README updates.
