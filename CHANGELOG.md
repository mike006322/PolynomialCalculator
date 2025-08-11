# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [0.3.0] - 2025-08-11
### Summary
This release delivers the structural migration of the core polynomial engine from the earlier term-matrix representation to a unified sparse dictionary keyed by immutable `Monomial` objects. The change simplifies invariants, reduces memory churn, and enables new micro-optimizations (hash caching, early scalar/zero fast paths). Medium and large polynomial multiplications observe double‑digit percentage speedups while maintaining numerical correctness (full test suite: 171 passed, 1 skipped).

### Added
- Benchmark comparison utility script `benchmarks/compare_benchmarks.py` (CSV diff for two pytest-benchmark JSON files) to streamline performance tracking.

### Changed
- Core representation: replaced term matrix with sparse map `{Monomial -> coefficient}`; removed redundant dual storage, simplifying arithmetic pipelines and lowering overhead in alignment and filtering.
- Optimized polynomial multiplication and scalar/zero/constant fast paths (cached Monomial hash, early exits) yielding ~15–17% speedup for medium/large multiplies (50 & 200 term benchmarks) and parity for tiny cases.
- Refactored `Polynomial.__mul__` for clearer fast path ordering (zero, one, constant * poly, variable alignment) minimizing temporary allocations and repeated coercion.

### Fixed
- Resolved indentation regressions introduced during iterative optimization; restored green test suite.
- Eliminated deepcopy failure for `Monomial` by removing conflicting `__slots__` usage with frozen dataclass while retaining cached hash semantics.

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
 - Core polynomial representation migrated from term-matrix structure to a unified sparse map (Monomial -> coefficient) for faster arithmetic and simpler invariants.
