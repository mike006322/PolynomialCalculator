import os
import random

import pytest


@pytest.fixture(autouse=True)
def _deterministic_env():
    # Ensure deterministic behavior for benchmarks
    os.environ.setdefault("POLYCALC_DEBUG", "0")
    random.seed(42)
    try:
        import numpy as np  # type: ignore

        np.random.seed(42)
    except Exception:
        pass
    yield
