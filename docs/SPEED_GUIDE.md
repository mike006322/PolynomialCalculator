# Speed Changes Guide

A lightweight checklist and process to document and reproduce performance changes.

## Checklist
- Scenario
  - Operation(s) under test (e.g., `__mul__`, `division_algorithm`, Groebner)
  - Inputs: degree, terms, variables, field p (or p=0), and fixed RNG seed
  - Display/logging: `POLYCALC_DEBUG=0`; choose numeric display mode (`--rational` recommended)
- Measurement
  - Use `pytest-benchmark`: ≥10 warmups, ≥50 rounds; report mean/std/CI
  - Build inputs outside the timed function; avoid I/O
  - Repeat best-of-3 if noisy
- Environment
  - OS/CPU, Python version, dependency versions (numpy/scipy), commit/tag
- Report
  - One-line summary: “X% faster” with absolute ms numbers
  - Scenario + method in one paragraph
  - Before → after table (or two lines)
  - Repro command

## Running benchmarks
- Install: `pip install -e .[dev]`
- All: `pytest -q benchmarks --benchmark-only`
- Single: `pytest -q benchmarks/test_poly_ops_bench.py::test_mul_benchmark[200] --benchmark-only`
- Save/compare:
  - `pytest benchmarks --benchmark-only --benchmark-save=run_A`
  - `pytest benchmarks --benchmark-only --benchmark-compare`

## PR template snippet
- Performance: Multiply two random monic polynomials (deg=200), seed=42.
- Method: pytest-benchmark, 10 warmup, 50 rounds, best-of-3.
- Results: 18.4 ms → 11.2 ms (−39.1%).
- Repro: `pytest -q benchmarks/test_poly_ops_bench.py::test_mul_benchmark[200] --benchmark-only`
