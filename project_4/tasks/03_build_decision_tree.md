# Task 3: Implement tree.py — ID3-style recursive decision tree build

# Context: Build the decision tree using the classic information-gain-driven ID3
approach, using information.py's best_attribute() to pick the splitting attribute at
every node. This is implemented in src/tree.py.

# Node representation: a plain Node class/struct with fields:
- attribute: the attribute name split on at this node, or None if this is a leaf.
- branches: dict mapping {0: child_node, 1: child_node}, empty for leaves.
- label: the predicted Decision ("Yes"/"No") if this is a leaf, else None.

# Build algorithm (ID3):
def build_tree(rows, attributes, label, default_label=None):
    If rows is empty: return a leaf with label = default_label (majority label of the
        parent node's rows — this is why the caller passes it down).
    If all rows share the same Decision value: return a leaf with that label.
    If attributes is empty (all attributes already used on this path): return a leaf
        with label = majority_label(rows).
    Otherwise:
        best = best_attribute(rows, attributes, label)
        majority = majority_label(rows)  # passed to children as their default_label
        node = Node(attribute=best)
        for value in (0, 1):
            subset = [r for r in rows if r[best] == value]
            remaining_attrs = [a for a in attributes if a != best]
            node.branches[value] = build_tree(subset, remaining_attrs, label, majority)
        return node

majority_label(rows) ties (exactly 50/50 split) are broken deterministically by
collections.Counter.most_common(1) — first-seen class in `rows` order wins.

# Other functions needed in tree.py:
- predict(node, row) -> "Yes"/"No": walk the tree from root using row[attribute] to
  pick 0/1 branch until a leaf is hit, return its label.
- tree_size(node) -> int: total node count (internal + leaf nodes).
- tree_depth(node) -> int: max root-to-leaf path length (a single leaf root has depth 0).
- accuracy(node, test_rows, label) -> float: fraction of test_rows where predict()
  matches the row's true label.
