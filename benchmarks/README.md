# Benchmarks

This folder contains repeatable benchmarks to track performance changes over time.

- Tooling: pytest-benchmark
- Determinism: fixed RNG seeds; inputs built outside timed code
- Output: mean, stddev, rounds; JSON export available via pytest-benchmark options

## How to run

- Install dev deps:
  - pip install -e .[dev]
- Run all benchmarks:
  - pytest -q benchmarks --benchmark-only
- Run a single case:
  - pytest -q benchmarks/test_poly_ops_bench.py::test_mul_deg_200 --benchmark-only
- Save/compare runs (optional):
  - pytest benchmarks --benchmark-only --benchmark-save=run_$(date +%Y%m%d)
  - pytest benchmarks --benchmark-only --benchmark-compare

