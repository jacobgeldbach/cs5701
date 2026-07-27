#!/usr/bin/env python3
"""Aggregate the per-trial results.csv (written by src/main.py) and plot, for each
of accuracy / precision / recall, an error-vs-training-size graph with a training
curve and a test curve. Also plots tree-size-vs-training-size. See
tasks/07_analyze_and_plot.md for the full spec.

Error is defined per metric so "lower is better" on every graph:
    accuracy graph  -> 1 - accuracy   (misclassification rate)
    precision graph -> 1 - precision  (false-discovery rate)
    recall graph    -> 1 - recall     (miss rate; the robot's costliest error)

Run with the venv interpreter (matplotlib lives there):
    python analyze.py
"""
import argparse
import csv
import glob
import os
import statistics
import sys
from collections import Counter, defaultdict

# Per-trial CSVs carry train/test confusion-matrix counts; everything (accuracy,
# precision, recall) is derived from these. Used to tell trial files from summary.csv.
RESULT_FIELDS = {"size", "trial",
                 "train_tp", "train_fn", "train_fp", "train_tn",
                 "test_tp", "test_fn", "test_fp", "test_tn",
                 "tree_size", "tree_depth", "root_attribute"}

import matplotlib
matplotlib.use("Agg")  # no display; write PNGs straight to disk
import matplotlib.pyplot as plt

# CVD-safe categorical slots 1 and 2: training curve vs. test curve.
_TRAIN_STYLE = {"color": "#2a78d6", "marker": "o", "label": "Training set"}
_TEST_STYLE = {"color": "#008300", "marker": "s", "label": "Test set"}


def _int_or_none(s):
    s = s.strip()
    return int(s) if s else None


def _counts(row, split):
    """(tp, fn, fp, tn) for 'train'/'test', or None when blank (no test set)."""
    vals = tuple(_int_or_none(row[f"{split}_{k}"]) for k in ("tp", "fn", "fp", "tn"))
    return None if any(v is None for v in vals) else vals


def load_results(results_dir):
    """Read every per-trial CSV in results_dir (the auto-named
    <size>_<trials>_<datestamp>.csv files main.py writes) and combine their rows.
    Non-trial files (e.g. the summary.csv this script writes) are skipped by header."""
    rows = []
    paths = sorted(glob.glob(os.path.join(results_dir, "*.csv")))
    used = []
    for path in paths:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or not RESULT_FIELDS.issubset(reader.fieldnames):
                continue  # skip summary.csv or anything that isn't per-trial output
            for r in reader:
                rows.append({
                    "size": int(r["size"]),
                    "trial": int(r["trial"]),
                    "train": _counts(r, "train"),
                    "test": _counts(r, "test"),  # None on a full-size (no test) run
                    "tree_size": int(r["tree_size"]),
                    "tree_depth": int(r["tree_depth"]),
                    "root_attribute": r["root_attribute"],
                })
        used.append(os.path.basename(path))
    if used:
        print(f"Read {len(rows)} trials from {len(used)} file(s): {', '.join(used)}")
    return rows


def _metrics(counts):
    """(accuracy, precision, recall) from (tp, fn, fp, tn); each None if undefined
    (precision when nothing is predicted positive, recall when there are no actual
    positives in the sample)."""
    if counts is None:
        return None, None, None
    tp, fn, fp, tn = counts
    total = tp + fn + fp + tn
    acc = (tp + tn) / total if total else None
    prec = tp / (tp + fp) if (tp + fp) else None
    rec = tp / (tp + fn) if (tp + fn) else None
    return acc, prec, rec


def _mean(vals):
    vals = [v for v in vals if v is not None]  # drop undefined/blank trials
    return statistics.mean(vals) if vals else None


def summarize(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[r["size"]].append(r)

    summary = []
    for size, recs in sorted(groups.items()):
        train = [_metrics(r["train"]) for r in recs]
        test = [_metrics(r["test"]) for r in recs]
        summary.append({
            "size": size,
            "n_trials": len(recs),
            "train_accuracy": _mean(m[0] for m in train),
            "train_precision": _mean(m[1] for m in train),
            "train_recall": _mean(m[2] for m in train),
            "test_accuracy": _mean(m[0] for m in test),
            "test_precision": _mean(m[1] for m in test),
            "test_recall": _mean(m[2] for m in test),
            "mean_tree_size": statistics.mean(r["tree_size"] for r in recs),
            "mean_tree_depth": statistics.mean(r["tree_depth"] for r in recs),
            "top_root_attribute": Counter(
                r["root_attribute"] for r in recs).most_common(1)[0][0],
        })
    return summary


def _fmt(v):
    return f"{v:.3f}" if v is not None else "n/a"


def print_table(summary):
    hdr = (f"{'size':>5} {'tr_acc':>7} {'tr_prec':>8} {'tr_rec':>7}  "
           f"{'te_acc':>7} {'te_prec':>8} {'te_rec':>7}  {'tree_sz':>8}")
    print("\n" + hdr)
    print("-" * len(hdr))
    for s in summary:
        print(f"{s['size']:>5} {_fmt(s['train_accuracy']):>7} "
              f"{_fmt(s['train_precision']):>8} {_fmt(s['train_recall']):>7}  "
              f"{_fmt(s['test_accuracy']):>7} {_fmt(s['test_precision']):>8} "
              f"{_fmt(s['test_recall']):>7}  {s['mean_tree_size']:>8.1f}")
    print()


def write_summary(summary, path):
    fields = ["size", "n_trials",
              "train_accuracy", "train_precision", "train_recall",
              "test_accuracy", "test_precision", "test_recall",
              "mean_tree_size", "mean_tree_depth", "top_root_attribute"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(summary)
    print(f"Wrote summary CSV -> {path}")


def _new_axes(ylabel, title):
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    ax.set_xlabel("Training set size (examples)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, color="#e1e0d9", linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return fig, ax


def _plot_error(summary, train_key, test_key, ylabel, title, path):
    """One error-vs-size graph with a training curve and a test curve. Error is
    1 - metric, so lower is better. Plots means only (no error bars)."""
    xs = sorted({s["size"] for s in summary})
    drawn = False
    fig, ax = _new_axes(ylabel, title)
    for key, style in ((train_key, _TRAIN_STYLE), (test_key, _TEST_STYLE)):
        series = [(s["size"], 1 - s[key]) for s in summary if s[key] is not None]
        if not series:
            continue
        sx = [p[0] for p in series]
        sy = [p[1] for p in series]
        ax.plot(sx, sy, color=style["color"], marker=style["marker"],
                markersize=8, linewidth=2, label=style["label"])
        drawn = True
    if not drawn:
        plt.close(fig)
        print(f"Skipped graph {path} -- no data points.")
        return
    ax.set_xticks(xs)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    print(f"Wrote graph -> {path}")


def _plot_tree_size(summary, path):
    pts = [s for s in summary if s["mean_tree_size"] is not None]
    if not pts:
        print(f"Skipped graph {path} -- no data points.")
        return
    xs = [s["size"] for s in pts]
    ys = [s["mean_tree_size"] for s in pts]
    fig, ax = _new_axes("Mean tree size (node count)",
                        "Decision tree size vs. training set size")
    ax.plot(xs, ys, color=_TRAIN_STYLE["color"], marker="o",
            markersize=8, linewidth=2)
    ax.set_xticks(xs)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    print(f"Wrote graph -> {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-dir", default="results",
                    help="directory of per-trial CSVs written by src/main.py")
    ap.add_argument("--summary", default="results/summary.csv",
                    help="aggregate summary CSV output path")
    ap.add_argument("--acc-out", default="results/accuracy_error_vs_size.png",
                    help="accuracy-error-vs-size graph PNG output path")
    ap.add_argument("--prec-out", default="results/precision_error_vs_size.png",
                    help="precision-error-vs-size graph PNG output path")
    ap.add_argument("--rec-out", default="results/recall_error_vs_size.png",
                    help="recall-error-vs-size graph PNG output path")
    ap.add_argument("--size-out", default="results/tree_size_vs_size.png",
                    help="tree-size-vs-size graph PNG output path")
    args = ap.parse_args()

    rows = load_results(args.results_dir)
    if not rows:
        print(f"No per-trial CSVs found in {args.results_dir}/ -- run src/main.py first.",
              file=sys.stderr)
        return 1

    summary = summarize(rows)
    print_table(summary)
    write_summary(summary, args.summary)
    _plot_error(summary, "train_accuracy", "test_accuracy",
                "Error (1 - accuracy)",
                "Decision tree accuracy error vs. training set size", args.acc_out)
    _plot_error(summary, "train_precision", "test_precision",
                "Error (1 - precision)",
                "Decision tree precision error vs. training set size", args.prec_out)
    _plot_error(summary, "train_recall", "test_recall",
                "Error (1 - recall)",
                "Decision tree recall error vs. training set size", args.rec_out)
    _plot_tree_size(summary, args.size_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
