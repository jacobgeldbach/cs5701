#!/usr/bin/env python3
"""Aggregate min-conflicts run logs and plot a size-vs-iterations convergence graph.

Expected layout (produced by the batch runs):

    project_3/
      size_0_data/
        run_1_size_0.log        <- 4-neighbor
        run_1_size_0_diag.log   <- 8-neighbor (diagonals)
        ...
      size_1_data/
      ...
      size_4_data/

Each log holds one GenerationStats block, e.g.:

    Min-Conflicts Results:
      Grid              : 200x200 (4-neighbor)
      Mode              : classic (random conflicted cell)
      Solved            : False
      Steps             : 120590
      ...

For every (size, diagonals) group this reports the success/failure counts and the
mean iterations-to-convergence over SUCCESSES ONLY, writes a summary CSV, and
renders one convergence graph: x = map size, y = mean iterations, two series
(diagonals on / off).

Run with the venv interpreter (matplotlib lives there):
    .venv/bin/python analyze.py
"""
import argparse
import csv
import glob
import os
import re
import statistics
import sys

import matplotlib
matplotlib.use("Agg")  # no display; write a PNG straight to disk
import matplotlib.pyplot as plt

# size index -> grid dimension, mirrors _SIZES in src/main.py.
_SIZES = [50, 75, 100, 150, 200]

# CVD-safe categorical pair from the dataviz reference palette (slots 1 and 8),
# with distinct marker shapes so the two series never rely on color alone.
_STYLE = {
    False: {"color": "#2a78d6", "marker": "o", "label": "4-neighbor (no diagonals)"},
    True:  {"color": "#eb6834", "marker": "s", "label": "8-neighbor (diagonals)"},
}

# Pull "Field : value" out of a stats block.
_FIELD = {
    "solved":   re.compile(r"Solved\s*:\s*(True|False)"),
    "steps":    re.compile(r"Steps\s*:\s*(\d+)"),
    "initial":  re.compile(r"Initial conflicts\s*:\s*(\d+)"),
    "final":    re.compile(r"Final conflicts\s*:\s*(\d+)"),
    "runtime":  re.compile(r"Runtime\s*:\s*([\d.]+)"),
    "neighbor": re.compile(r"\((\d+)-neighbor\)"),
}


class Record:
    __slots__ = ("size", "diag", "run", "solved", "steps", "initial",
                 "final", "runtime", "path")


def parse_log(path):
    """Parse one log file into a Record, or return None if it isn't a valid run
    (empty, a crash traceback, or missing the fields we need).

    Layout is path-based: size comes from the `size_N/` folder and diagonals
    from a `diagonals/` subfolder; the filename is just `run_N.log`."""
    name = os.path.basename(path)

    # size index from the `size_N` path component.
    m_size = re.search(r"size_(\d+)", path)
    if not m_size:
        return None
    size = int(m_size.group(1))
    # diagonals iff a `diagonals` directory appears anywhere in the path.
    parts = os.path.normpath(path).split(os.sep)
    diag = "diagonals" in parts
    m_run = re.search(r"run_(\d+)", name)
    run = int(m_run.group(1)) if m_run else -1

    try:
        with open(path, "r", errors="replace") as f:
            text = f.read()
    except OSError:
        return None

    solved = _FIELD["solved"].search(text)
    steps = _FIELD["steps"].search(text)
    if not solved or not steps:
        return None  # not a completed run (e.g. a pygame ImportError log)

    rec = Record()
    rec.size = size
    rec.diag = diag
    rec.run = run
    rec.solved = solved.group(1) == "True"
    rec.steps = int(steps.group(1))
    rec.initial = int(_FIELD["initial"].search(text).group(1)) if _FIELD["initial"].search(text) else None
    rec.final = int(_FIELD["final"].search(text).group(1)) if _FIELD["final"].search(text) else None
    rt = _FIELD["runtime"].search(text)
    rec.runtime = float(rt.group(1)) if rt else None
    rec.path = path

    # Cross-check the neighbor count in the file against the filename flag.
    nb = _FIELD["neighbor"].search(text)
    if nb:
        expected = 8 if diag else 4
        if int(nb.group(1)) != expected:
            print(f"  ! {name}: filename says {'diag' if diag else 'no-diag'} "
                  f"but file reports {nb.group(1)}-neighbor", file=sys.stderr)
    return rec


def collect(data_dir):
    """Find and parse every run log under data_dir. Returns (records, bad_files)."""
    seen = set()
    paths = []
    for p in glob.glob(os.path.join(data_dir, "**", "*.log"), recursive=True):
        ap = os.path.abspath(p)
        if ap not in seen:
            seen.add(ap)
            paths.append(p)

    records, bad = [], []
    for p in sorted(paths):
        rec = parse_log(p)
        (records.append if rec else bad.append)(rec if rec else p)
    return records, bad


def summarize(records):
    """Group records by (size, diag) -> dict of aggregate stats."""
    groups = {}
    for r in records:
        groups.setdefault((r.size, r.diag), []).append(r)

    rows = []
    for (size, diag), recs in sorted(groups.items()):
        succ = [r for r in recs if r.solved]
        fail = [r for r in recs if not r.solved]
        steps_succ = [r.steps for r in succ]
        rt_succ = [r.runtime for r in succ if r.runtime is not None]
        rows.append({
            "size_index": size,
            "dim": _SIZES[size] if size < len(_SIZES) else size,
            "diagonals": diag,
            "n_runs": len(recs),
            "n_success": len(succ),
            "n_fail": len(fail),
            "success_rate": len(succ) / len(recs) if recs else 0.0,
            "mean_steps_success": statistics.mean(steps_succ) if steps_succ else None,
            "median_steps_success": statistics.median(steps_succ) if steps_succ else None,
            "stdev_steps_success": statistics.pstdev(steps_succ) if len(steps_succ) > 1 else 0.0,
            "mean_runtime_success": statistics.mean(rt_succ) if rt_succ else None,
        })
    return rows


def print_table(rows):
    hdr = (f"{'size':>5} {'dim':>5} {'diag':>5} {'runs':>5} {'ok':>4} "
           f"{'fail':>5} {'succ%':>6} {'mean_iters':>11} {'median':>9} {'mean_rt(s)':>11}")
    print("\n" + hdr)
    print("-" * len(hdr))
    for r in rows:
        mi = f"{r['mean_steps_success']:.1f}" if r["mean_steps_success"] is not None else "n/a"
        md = f"{r['median_steps_success']:.0f}" if r["median_steps_success"] is not None else "n/a"
        rt = f"{r['mean_runtime_success']:.1f}" if r["mean_runtime_success"] is not None else "n/a"
        print(f"{r['size_index']:>5} {r['dim']:>5} {str(r['diagonals']):>5} "
              f"{r['n_runs']:>5} {r['n_success']:>4} {r['n_fail']:>5} "
              f"{100 * r['success_rate']:>5.1f}% {mi:>11} {md:>9} {rt:>11}")
    print()


def write_csv(rows, path):
    fields = ["size_index", "dim", "diagonals", "n_runs", "n_success", "n_fail",
              "success_rate", "mean_steps_success", "median_steps_success",
              "stdev_steps_success", "mean_runtime_success"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote summary CSV -> {path}")


def plot(rows, path, title):
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    for diag in (False, True):
        pts = sorted(
            [(r["dim"], r["mean_steps_success"]) for r in rows
             if r["diagonals"] == diag and r["mean_steps_success"] is not None]
        )
        if not pts:
            continue
        xs, ys = zip(*pts)
        style = _STYLE[diag]
        ax.plot(xs, ys, color=style["color"], marker=style["marker"],
                markersize=8, linewidth=2, label=style["label"])

    ax.set_xlabel("Map size (grid dimension, N×N cells)")
    ax.set_ylabel("Mean iterations to convergence (successful runs)")
    ax.set_title(title)
    ax.set_xticks(_SIZES)
    ax.grid(True, color="#e1e0d9", linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.legend(frameon=False)

    fig.tight_layout()
    fig.savefig(path)
    print(f"Wrote convergence graph -> {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", default=".",
                    help="directory holding the size_*_data/ folders (default: cwd)")
    ap.add_argument("--csv", default="summary.csv", help="summary CSV output path")
    ap.add_argument("--out", default="convergence.png", help="graph PNG output path")
    ap.add_argument("--title", default="Min-conflicts convergence vs. map size",
                    help="graph title")
    args = ap.parse_args()

    records, bad = collect(args.data_dir)
    print(f"Parsed {len(records)} run logs; {len(bad)} file(s) skipped "
          f"(empty / crashed / unrecognized).")
    if bad:
        for p in bad[:10]:
            print(f"  skipped: {p}")
        if len(bad) > 10:
            print(f"  ... and {len(bad) - 10} more")
    if not records:
        print("No usable run logs found -- nothing to summarize.", file=sys.stderr)
        return 1

    rows = summarize(records)
    print_table(rows)
    write_csv(rows, args.csv)
    plot(rows, args.out, args.title)
    return 0


if __name__ == "__main__":
    sys.exit(main())
