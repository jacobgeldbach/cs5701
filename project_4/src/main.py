#!/usr/bin/env python3
"""Experiment sweep driver: builds decision trees over random train/test splits of
varying training-set size and logs per-trial results. See
tasks/05_experiment_sweep_and_logging.md for the full spec.

Run from project_4/:
    python src/main.py --sizes 10,20,50,80 --trials 10
"""
import argparse
import csv
import os
import random
import statistics
import sys

from sampling import load_dataset, train_test_split
from tree import build_tree, majority_label, predict, tree_size, tree_depth, accuracy

DEFAULT_DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "Problem4DecisionTreeData.CSV",
)
DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "results", "results.csv",
)

RESULT_FIELDS = ["size", "trial", "accuracy", "tree_size", "tree_depth", "root_attribute"]


def parse_sizes(args):
    if args.sizes:
        return [int(s) for s in args.sizes.split(",")]
    if args.min_size is None or args.max_size is None or args.step is None:
        raise SystemExit("Provide --sizes, or all of --min-size/--max-size/--step")
    return list(range(args.min_size, args.max_size + 1, args.step))


def run_sweep(rows, attributes, label, sizes, trials, rng):
    records = []
    for size in sizes:
        size_accs, size_tree_sizes = [], []
        for trial in range(trials):
            train_rows, test_rows = train_test_split(rows, size, rng)
            root = build_tree(train_rows, attributes, label, majority_label(train_rows, label))
            acc = accuracy(root, test_rows, label)
            record = {
                "size": size,
                "trial": trial,
                "accuracy": acc,
                "tree_size": tree_size(root),
                "tree_depth": tree_depth(root),
                "root_attribute": root.attribute,
            }
            records.append(record)
            size_accs.append(acc)
            size_tree_sizes.append(record["tree_size"])
        print(
            f"size={size:>3}: mean acc={statistics.mean(size_accs):.3f}  "
            f"mean tree_size={statistics.mean(size_tree_sizes):.1f}"
        )
    return records


def write_results(records, out_path):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} trial results -> {out_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default=DEFAULT_DATA, help="path to the CSV data file")
    ap.add_argument("--sizes", default=None, help='comma-separated training sizes, e.g. "10,20,50,80"')
    ap.add_argument("--min-size", type=int, default=None)
    ap.add_argument("--max-size", type=int, default=None)
    ap.add_argument("--step", type=int, default=None)
    ap.add_argument("--trials", type=int, default=10, help="random trials per size (default 10)")
    ap.add_argument("--seed", type=int, default=None, help="RNG seed for reproducibility")
    ap.add_argument("--out", default=DEFAULT_OUT, help="path to write per-trial results CSV")
    ap.add_argument("--visualize", action="store_true", help="also open a pygame tree view")
    ap.add_argument("--visualize-size", type=int, default=None,
                     help="training size for --visualize (default: all rows)")
    args = ap.parse_args()

    rows, attributes, label = load_dataset(args.data)
    rng = random.Random(args.seed)

    if args.sizes or (args.min_size is not None):
        sizes = parse_sizes(args)
        records = run_sweep(rows, attributes, label, sizes, args.trials, rng)
        write_results(records, args.out)

    if args.visualize:
        from visualization import show_tree
        vis_size = args.visualize_size or len(rows)
        if vis_size >= len(rows):
            root = build_tree(rows, attributes, label, majority_label(rows, label))
            vis_size = len(rows)
        else:
            train_rows, _ = train_test_split(rows, vis_size, rng)
            root = build_tree(train_rows, attributes, label, majority_label(train_rows, label))
        show_tree(root, attributes, train_size=vis_size)

    return 0


if __name__ == "__main__":
    sys.exit(main())
