# Task 2: Implement information.py — entropy and information gain

# Context: This is the core calculation module, implemented standalone in
src/information.py so it can be imported and unit-tested independently of the tree
builder. It computes how much information is gained about the class label ("Decision")
by knowing the value of a given attribute, over a given subset of examples (rows).

# Entropy: I(p(v1) ... p(vn)) = -sum_i p(vi) * log2(p(vi))
For a set of rows, the class distribution is the set of proportions of each Decision
value ("Yes" count / total, "No" count / total). A subset with 0 rows or a pure subset
(all one class) has entropy 0. Skip any p(vi) == 0 term in the sum (0*log2(0) is
defined as 0, do not call log2(0)).

# Functions:
- information(rows, label) -> float: computes I() over the class distribution of rows.
- information_gain(rows, attribute, label) -> float: information(rows) minus the
  weighted average information of the two partitions of rows produced by splitting on
  `attribute` (attribute == 0 partition and attribute == 1 partition), weighted by
  partition size / len(rows).
- best_attribute(rows, attributes, label) -> str: returns the attribute (from the given
  candidate list) with the maximum information_gain over rows. Ties are broken by
  picking whichever attribute appears first in the `attributes` list (i.e. iterate the
  list in order and keep the first strictly-greater gain found).

No pygame/matplotlib dependency in this file — it is pure calculation.
