# Task 4: Random train/test sampling

# Context: For a given training set size N, randomly select N of the 100 examples as
the training set; the remaining (100 - N) examples are the held-out test set for that
trial (per-class discussion: train on a random subset, measure accuracy on what's left
over). Implemented as train_test_split() in src/sampling.py, alongside load_dataset()
from Task 1.

# Function: train_test_split(rows, train_size, rng) -> (train_rows, test_rows)
- rng is a random.Random instance (caller controls/seeds it so experiment runs are
  reproducible when a --seed CLI arg is given, but distinct across trials).
- Uses rng.sample(rows, train_size) to draw the training rows without replacement, the
  rest (by identity) are the test rows.
- train_size must be between 1 and len(rows) - 1 inclusive so there is always at least
  one test example left; raise ValueError otherwise.
