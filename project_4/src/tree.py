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
