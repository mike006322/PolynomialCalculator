import json
import sys
from pathlib import Path

def load(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

def extract(measure):
    return {b['name']: b['stats']['mean'] for b in measure['benchmarks']}

def main():
    if len(sys.argv) < 3:
        print("Usage: python benchmarks/compare_benchmarks.py OLD.json NEW.json [FILTER_SUBSTR]")
        return 1
    old_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])
    filt = sys.argv[3] if len(sys.argv) > 3 else None
    old = extract(load(old_path))
    new = extract(load(new_path))
    names = sorted(new.keys())
    print("name,old_mean_s,new_mean_s,delta_pct,speedup_x")
    for name in names:
        if name not in old:
            continue
        if filt and filt not in name:
            continue
        o = old[name]
        n = new[name]
        if o == 0:
            continue
        delta_pct = (n - o) / o * 100.0
        speed = o / n if n else float('inf')
        print(f"{name},{o:.6e},{n:.6e},{delta_pct:+.2f},{speed:.3f}")
    return 0

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
