"""Information (entropy) and information-gain calculations for the decision tree
builder.

Pure calculation module -- no pygame/matplotlib dependency. See
tasks/02_information_gain.md for the full spec.
"""
import math
from collections import Counter


def information(rows, label):
    """I(p(v1) ... p(vn)) = -sum_i p(vi) * log2(p(vi)) over the class distribution
    of `label` values in `rows`. Empty rows -> 0.0."""
    if not rows:
        return 0.0
    counts = Counter(r[label] for r in rows)
    total = len(rows)
    total_information = 0.0
    for count in counts.values():
        p = count / total
        if p > 0:
            total_information -= p * math.log2(p)
    return total_information


def information_gain(rows, attribute, label):
    """information(rows) minus the weighted average information of the two
    partitions produced by splitting rows on `attribute` (0-branch and 1-branch)."""
    if not rows:
        return 0.0
    parent_information = information(rows, label)
    total = len(rows)
    weighted = 0.0
    for value in (0, 1):
        subset = [r for r in rows if r[attribute] == value]
        if subset:
            weighted += (len(subset) / total) * information(subset, label)
    return parent_information - weighted


def best_attribute(rows, attributes, label):
    """Attribute (from `attributes`) with the maximum information_gain over rows.
    Ties are broken by picking whichever attribute appears first in `attributes`."""
    best_attr = None
    best_gain = float("-inf")
    for attr in attributes:
        gain = information_gain(rows, attr, label)
        if gain > best_gain:
            best_gain = gain
            best_attr = attr
    return best_attr
