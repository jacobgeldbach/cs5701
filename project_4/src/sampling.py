"""CSV loading and random train/test splitting. See tasks/01_data_read_and_representation.md
and tasks/04_train_test_sampling.md for the full spec."""
import csv

LABEL = "Decision"


def load_dataset(path):
    """Returns (rows, attributes, label).

    rows: list of dict, one per example -- attribute name -> 0/1 int, plus
          LABEL -> "Yes"/"No" string. The "Example" id column is dropped.
    attributes: ordered list of the 7 attribute name strings, in header order
                (this fixed order is also used to break information-gain ties).
    label: the LABEL constant ("Decision").
    """
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        attributes = [name for name in fieldnames if name not in ("Example", LABEL)]
        rows = []
        for raw in reader:
            row = {attr: int(raw[attr]) for attr in attributes}
            row[LABEL] = raw[LABEL]
            rows.append(row)
    return rows, attributes, LABEL


def train_test_split(rows, train_size, rng):
    """Randomly draw `train_size` rows (without replacement) as the training set;
    the rest are the held-out test set. `rng` is a random.Random instance so
    experiment sweeps can be seeded/reproduced."""
    if not (1 <= train_size <= len(rows) - 1):
        raise ValueError(
            f"train_size must be between 1 and {len(rows) - 1} (got {train_size})"
        )
    train_rows = rng.sample(rows, train_size)
    train_ids = {id(r) for r in train_rows}
    test_rows = [r for r in rows if id(r) not in train_ids]
    return train_rows, test_rows
