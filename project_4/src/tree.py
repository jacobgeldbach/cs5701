"""ID3-style recursive decision tree build and evaluation. See
tasks/03_build_decision_tree.md for the full spec."""
from collections import Counter

from information import best_attribute


class Node:
    __slots__ = ("attribute", "branches", "label")

    def __init__(self, attribute=None, label=None):
        self.attribute = attribute
        self.branches = {}
        self.label = label

    @property
    def is_leaf(self):
        return self.attribute is None


def majority_label(rows, label):
    """Most common label value in rows. Ties broken by first-seen order
    (Counter.most_common is stable on insertion order for equal counts)."""
    counts = Counter(r[label] for r in rows)
    return counts.most_common(1)[0][0]


def build_tree(rows, attributes, label, default_label=None):
    if not rows:
        return Node(label=default_label)

    labels = {r[label] for r in rows}
    if len(labels) == 1:
        return Node(label=next(iter(labels)))

    if not attributes:
        return Node(label=majority_label(rows, label))

    best = best_attribute(rows, attributes, label)
    majority = majority_label(rows, label)
    node = Node(attribute=best)
    remaining_attrs = [a for a in attributes if a != best]
    for value in (0, 1):
        subset = [r for r in rows if r[best] == value]
        node.branches[value] = build_tree(subset, remaining_attrs, label, majority)
    return node


def predict(node, row):
    while not node.is_leaf:
        node = node.branches[row[node.attribute]]
    return node.label


def tree_size(node):
    if node.is_leaf:
        return 1
    return 1 + sum(tree_size(child) for child in node.branches.values())


def tree_depth(node):
    if node.is_leaf:
        return 0
    return 1 + max(tree_depth(child) for child in node.branches.values())


def accuracy(node, test_rows, label):
    if not test_rows:
        return None
    correct = sum(1 for r in test_rows if predict(node, r) == r[label])
    return correct / len(test_rows)


def confusion_counts(node, test_rows, label, positive):
    """Confusion-matrix counts on test_rows with `positive` as the positive class
    (here "ask for help"). Returns (tp, fn, fp, tn), or None when there is no test
    set. A false negative -- the tree predicting "don't ask" when it should have
    asked -- is the robot's costliest error, so keeping FN separate lets analyze.py
    compute recall = tp / (tp + fn)."""
    if not test_rows:
        return None
    tp = fn = fp = tn = 0
    for r in test_rows:
        pred = predict(node, r)
        actual_pos = r[label] == positive
        pred_pos = pred == positive
        if actual_pos and pred_pos:
            tp += 1
        elif actual_pos and not pred_pos:
            fn += 1
        elif not actual_pos and pred_pos:
            fp += 1
        else:
            tn += 1
    return tp, fn, fp, tn
