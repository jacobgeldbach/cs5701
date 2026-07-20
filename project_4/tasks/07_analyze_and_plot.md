# Task 7: analyze.py — aggregate results.csv and plot accuracy/tree-size vs. training size

# Context: This mirrors the analyze.py pattern from project_3 (argparse-driven,
matplotlib Agg backend so no display is needed, CVD-safe styling), but reads directly
from the results CSV written by src/main.py's sweep (Task 5) instead of parsing text
run logs, since main.py can emit structured rows directly.

# CLI arguments (argparse):
--results   path to the per-trial results CSV (default: results/results.csv)
--summary   path to write the per-size aggregate summary CSV (default:
            results/summary.csv)
--acc-out   path for the accuracy-vs-training-size PNG (default:
            results/accuracy_vs_size.png)
--size-out  path for the tree-size-vs-training-size PNG (default:
            results/tree_size_vs_size.png)

# Aggregation: group the per-trial rows by `size`, compute for each size: n_trials,
mean/stdev accuracy, mean/stdev tree_size, mean/stdev tree_depth, and the most common
root_attribute (mode, with count) — this last one answers "does the root attribute
stay stable across random subsets of a given size?" Print a table to stdout (same
style as project_3's print_table) and write the aggregate rows to --summary.

# Plots (two separate PNGs, each: matplotlib Agg backend, figsize ~(7, 4.5), dpi 300,
gridlines, no top/right spines, legend, x-axis ticked at each tested size):
1. Accuracy vs. training set size: x = size, y = mean accuracy, with error bars
   (+/- stdev) across trials. Answers the "how does test accuracy change with more
   training data" question.
2. Tree size vs. training set size: x = size, y = mean tree_size (node count), with
   error bars (+/- stdev). Answers "do larger training sets produce larger, smaller,
   or same-sized trees" — the key question called out in the assignment.
