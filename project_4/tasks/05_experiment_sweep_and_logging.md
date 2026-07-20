# Task 5: main.py — experiment sweep CLI and results logging

# Context: This is the experiment driver in src/main.py. It sweeps over training set
sizes, runs multiple random trials per size, builds a tree per trial with tree.py,
measures its test accuracy and size, and logs one row per trial to a CSV for later
analysis by analyze.py (Task 7). It can also just build a single tree and hand it to
visualization.py (Task 6) to look at.

# CLI arguments (argparse):
--data       path to the CSV (default: data/Problem4DecisionTreeData.CSV)
--sizes      comma-separated list of training set sizes, e.g. "10,20,50,80"
             (mutually exclusive with --min-size/--max-size/--step)
--min-size, --max-size, --step   generate sizes as range(min, max+1, step) when
             --sizes is not given
--trials     number of random trials per size (default 10, per the "10+ trials" spec)
--seed       optional int to seed the RNG for reproducible sweeps
--out        path to write the per-trial results CSV (default: results/results.csv)
--visualize  optional flag: also build one tree (on a full-data or --visualize-size
             sized random training set) and open the pygame visualization window from
             Task 6
--visualize-size  training size to use when --visualize is passed (default: len(rows),
             i.e. train on everything)

# Sweep behavior:
For each size in the size list:
    For trial in range(trials):
        train_rows, test_rows = train_test_split(rows, size, rng)
        root = build_tree(train_rows, attributes, label, majority_label(train_rows))
        acc = accuracy(root, test_rows, label)
        record: {size, trial, accuracy: acc, tree_size: tree_size(root),
                 tree_depth: tree_depth(root), root_attribute: root.attribute}
Write every record as a row to the --out CSV (header: size,trial,accuracy,tree_size,
tree_depth,root_attribute), creating parent directories as needed.

Print a short progress line per size (e.g. "size=20: mean acc=0.83 mean tree_size=9.2")
so a run's progress is visible without waiting for analyze.py.
