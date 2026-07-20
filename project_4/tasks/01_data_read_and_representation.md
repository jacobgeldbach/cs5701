# Task 1: Read the CSV data and build the in-memory example representation

# Context: The data lives in data/Problem4DecisionTreeData.CSV. The header row is:
Example,Familiar Situation,In a hurry,Long Delay,Safe Situation,Confident,Safety Critical Decision,Asked Before,Decision
The first column ("Example") is just a run id and is not an attribute. The last column
("Decision") is the class label with string values "Yes"/"No" (Yes = ask for help,
No = robot decides on its own). The 7 attribute columns in between are all binary
(0/1). Build this in sampling.py in src/ as the shared data-loading module (also used
later by the train/test split task).

# Function: load_dataset(path) -> (rows, attributes, label)
- rows: a list of dict, one per example, each dict maps attribute name -> 0/1 int and
  "Decision" -> "Yes"/"No" string. The "Example" id column is dropped (not needed once
  loaded, order in the list is sufficient).
- attributes: the ordered list of the 7 attribute name strings exactly as they appear
  in the header (this fixed order is also used later to break information-gain ties,
  first attribute in this order wins).
- label: the string "Decision" (kept as a named constant so nothing hardcodes it twice).

Use the standard library csv module (csv.DictReader), no pandas dependency needed.
