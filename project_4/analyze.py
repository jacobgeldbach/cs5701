#!/usr/bin/env python3
"""Aggregate the per-trial results.csv (written by src/main.py) and plot
accuracy-vs-training-size and tree-size-vs-training-size graphs. See
tasks/07_analyze_and_plot.md for the full spec.

Run with the venv interpreter (matplotlib lives there):
    python analyze.py
"""
import argparse
import csv
import statistics
import sys
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")  # no display; write PNGs straight to disk
import matplotlib.pyplot as plt

# CVD-safe categorical color, single series (accuracy or tree size vs. size).
_STYLE = {"color": "#2a78d6", "marker": "o"}


def load_results(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            rows.append({
                "size": int(r["size"]),
                "trial": int(r["trial"]),
                "accuracy": float(r["accuracy"]),
                "tree_size": int(r["tree_size"]),
                "tree_depth": int(r["tree_depth"]),
                "root_attribute": r["root_attribute"],
            })
        return rows


def summarize(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[r["size"]].append(r)

    summary = []
    for size, recs in sorted(groups.items()):
        accs = [r["accuracy"] for r in recs]
        sizes = [r["tree_size"] for r in recs]
        depths = [r["tree_depth"] for r in recs]
        root_counts = Counter(r["root_attribute"] for r in recs)
        top_root, top_count = root_counts.most_common(1)[0]
        summary.append({
            "size": size,
            "n_trials": len(recs),
            "mean_accuracy": statistics.mean(accs),
            "stdev_accuracy": statistics.pstdev(accs) if len(accs) > 1 else 0.0,
            "mean_tree_size": statistics.mean(sizes),
            "stdev_tree_size": statistics.pstdev(sizes) if len(sizes) > 1 else 0.0,
            "mean_tree_depth": statistics.mean(depths),
            "stdev_tree_depth": statistics.pstdev(depths) if len(depths) > 1 else 0.0,
            "top_root_attribute": top_root,
            "top_root_attribute_count": top_count,
        })
    return summary


def print_table(summary):
    hdr = (f"{'size':>5} {'trials':>7} {'mean_acc':>9} {'std_acc':>8} "
           f"{'mean_tsize':>11} {'std_tsize':>10} {'top_root_attr':>22}")
    print("\n" + hdr)
    print("-" * len(hdr))
    for s in summary:
        print(f"{s['size']:>5} {s['n_trials']:>7} {s['mean_accuracy']:>9.3f} "
              f"{s['stdev_accuracy']:>8.3f} {s['mean_tree_size']:>11.1f} "
              f"{s['stdev_tree_size']:>10.1f} "
              f"{s['top_root_attribute'] + ' (' + str(s['top_root_attribute_count']) + ')':>22}")
    print()


def write_summary(summary, path):
    fields = ["size", "n_trials", "mean_accuracy", "stdev_accuracy",
              "mean_tree_size", "stdev_tree_size", "mean_tree_depth",
              "stdev_tree_depth", "top_root_attribute", "top_root_attribute_count"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(summary)
    print(f"Wrote summary CSV -> {path}")


def _plot(summary, y_key, err_key, ylabel, title, path):
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    xs = [s["size"] for s in summary]
    ys = [s[y_key] for s in summary]
    errs = [s[err_key] for s in summary]
    ax.errorbar(xs, ys, yerr=errs, color=_STYLE["color"], marker=_STYLE["marker"],
                markersize=8, linewidth=2, capsize=4)
    ax.set_xlabel("Training set size (examples)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(xs)
    ax.grid(True, color="#e1e0d9", linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(path)
    print(f"Wrote graph -> {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", default="results/results.csv",
                     help="per-trial results CSV written by src/main.py")
    ap.add_argument("--summary", default="results/summary.csv",
                     help="aggregate summary CSV output path")
    ap.add_argument("--acc-out", default="results/accuracy_vs_size.png",
                     help="accuracy-vs-training-size graph PNG output path")
    ap.add_argument("--size-out", default="results/tree_size_vs_size.png",
                     help="tree-size-vs-training-size graph PNG output path")
    args = ap.parse_args()

    rows = load_results(args.results)
    if not rows:
        print("No results found -- nothing to summarize.", file=sys.stderr)
        return 1

    summary = summarize(rows)
    print_table(summary)
    write_summary(summary, args.summary)
    _plot(summary, "mean_accuracy", "stdev_accuracy", "Mean test accuracy",
          "Decision tree test accuracy vs. training set size", args.acc_out)
    _plot(summary, "mean_tree_size", "stdev_tree_size", "Mean tree size (node count)",
          "Decision tree size vs. training set size", args.size_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
