#!/usr/bin/env python3
"""Experiment driver: builds decision trees over random train/test splits at a single
training-set size and logs per-trial results. Run once per size you want to test. See
tasks/05_experiment_sweep_and_logging.md for the full spec.

Run from project_4/:
    python src/main.py --size 20 --trials 15 --seed 42
    python src/main.py --size 20 --visualize      # also show the tree for this run
    python src/main.py                            # defaults to all examples (max)
"""
import argparse
import csv
import os
import random
import statistics
import sys
from datetime import datetime

from sampling import load_dataset, train_test_split, POSITIVE_LABEL
from tree import (build_tree, majority_label, predict, tree_size, tree_depth,
                  confusion_counts)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA = os.path.join(PROJECT_ROOT, "data", "Problem4DecisionTreeData.CSV")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

# {train,test}_{tp,fn,fp,tn} are the confusion-matrix counts with "ask for help"
# (POSITIVE_LABEL) as the positive class, logged for both the training set (the tree
# scored on its own rows) and the held-out test set. analyze.py derives accuracy,
# precision and recall for each split from these. test_* is blank on a full-size run
# (no held-out test set).
RESULT_FIELDS = ["size", "trial",
                 "train_tp", "train_fn", "train_fp", "train_tn",
                 "test_tp", "test_fn", "test_fp", "test_tn",
                 "tree_size", "tree_depth", "root_attribute"]


def run_size(rows, attributes, label, size, trials, rng):
    """Run `trials` random train/test splits at training-set `size` and return one
    record per trial. When size covers all rows there is no held-out test set, so the
    tree is built on everything and accuracy is left blank (still records tree stats)."""
    records = []
    full_data = size >= len(rows)
    size_accs, size_tree_sizes = [], []
    for trial in range(trials):
        if full_data:
            train_rows, test_rows = rows, []
        else:
            train_rows, test_rows = train_test_split(rows, size, rng)
        root = build_tree(train_rows, attributes, label, majority_label(train_rows, label))
        tr_tp, tr_fn, tr_fp, tr_tn = confusion_counts(root, train_rows, label, POSITIVE_LABEL)
        test_counts = confusion_counts(root, test_rows, label, POSITIVE_LABEL)  # None when empty
        te_tp, te_fn, te_fp, te_tn = test_counts if test_counts else (None, None, None, None)
        acc = ((te_tp + te_tn) / (te_tp + te_fn + te_fp + te_tn)) if test_counts else None
        record = {
            "size": min(size, len(rows)),
            "trial": trial,
            "train_tp": tr_tp, "train_fn": tr_fn, "train_fp": tr_fp, "train_tn": tr_tn,
            "test_tp": te_tp, "test_fn": te_fn, "test_fp": te_fp, "test_tn": te_tn,
            "tree_size": tree_size(root),
            "tree_depth": tree_depth(root),
            "root_attribute": root.attribute,
        }
        records.append(record)
        if acc is not None:
            size_accs.append(acc)
        size_tree_sizes.append(record["tree_size"])
    acc_str = f"{statistics.mean(size_accs):.3f}" if size_accs else "n/a (no test set)"
    print(
        f"size={min(size, len(rows)):>3}: mean acc={acc_str}  "
        f"mean tree_size={statistics.mean(size_tree_sizes):.1f}"
    )
    return records


def write_results(records, size, trials):
    """Write per-trial rows to results/<size>_<trials>_<datestamp>.csv (auto-named)."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(RESULTS_DIR, f"{size}_{trials}_{stamp}.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} trial results -> {out_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=DEFAULT_DATA, help="path to the CSV data file")
    ap.add_argument("--size", type=int, default=None,
                    help="training set size for this run (default: all examples / max)")
    ap.add_argument("--trials", type=int, default=10, help="random trials per size (default 10)")
    ap.add_argument("--seed", type=int, default=None, help="RNG seed for reproducibility")
    ap.add_argument("--visualize", action="store_true",
                    help="also open a pygame view of a tree built at --size")
    args = ap.parse_args()

    rows, attributes, label = load_dataset(args.data)
    rng = random.Random(args.seed)

    size = len(rows) if args.size is None else min(args.size, len(rows))

    records = run_size(rows, attributes, label, size, args.trials, rng)
    write_results(records, size, args.trials)

    if args.visualize:
        from visualization import show_tree
        if size >= len(rows):
            root = build_tree(rows, attributes, label, majority_label(rows, label))
        else:
            train_rows, _ = train_test_split(rows, size, rng)
            root = build_tree(train_rows, attributes, label, majority_label(train_rows, label))
        show_tree(root, attributes, train_size=size)

    return 0


if __name__ == "__main__":
    sys.exit(main())
