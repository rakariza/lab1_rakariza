# Lab 1: Grade Evaluator & Archiver

This project evaluates course grades from a CSV file and automates archiving
the grade data. It validates scores and assignment weights, calculates the
student's final grade and GPA, determines the final status, and identifies
eligible formative assignments for resubmission.

## Project files

- `grade-evaluator.py` — validates and evaluates the grade data.
- `grades.csv` — contains the assignment data used by the Python program.
- `organizer.sh` — archives the current CSV and creates a new empty CSV.
- `README.md` — explains how to use the project.

## Requirements

- Python 3
- Bash (Git Bash can be used on Windows)

No external Python packages are required.

## CSV format

The CSV must contain these four columns:

```csv
assignment,group,score,weight
```

The group must be either `Formative` or `Summative`. Scores must be from 0 to
100. Total assignment weights must equal 100, with exactly 60 assigned to the
Formative group and 40 assigned to the Summative group.

## Run the grade evaluator

1. Open this folder in Visual Studio Code.
2. Select **Terminal > New Terminal**.
3. Run:

```bash
python grade-evaluator.py
```

On Windows, if `python` is not recognized, use:

```bash
py grade-evaluator.py
```

When prompted, enter:

```text
grades.csv
```

You may also press Enter to use `grades.csv` automatically.

## Calculations and decisions

Each weighted assignment contributes:

```text
score × weight ÷ 100
```

The GPA formula is:

```text
GPA = (total grade ÷ 100) × 5.0
```

The student passes only when the Formative result and the Summative result are
both at least 50%. If the student fails, the program finds failed Formative
assignments with scores below 50%. The failed Formative assignment carrying the
highest weight is eligible for resubmission. Tied assignments are all shown.

## Run the organizer

The script moves the current `grades.csv`, so keep a backup when testing it.

On Windows, open the project in **Git Bash** and run:

```bash
bash organizer.sh
```

The script:

1. Creates an `archive` directory if needed.
2. Renames the current CSV using a timestamp.
3. Moves the renamed CSV into `archive`.
4. Creates a new empty `grades.csv`.
5. Adds the operation to `organizer.log`.

An archived filename looks like:

```text
grades_20260724-153000.csv
```

## Error handling

The evaluator displays a clear error instead of crashing when:

- the CSV is missing or empty;
- the CSV header is incomplete;
- a row is empty or contains invalid data;
- an assignment name is missing;
- the group name is invalid;
- a score is outside 0–100;
- a weight is not positive; or
- total weights do not follow the required 60/40 split.

The organizer reports an error if `grades.csv` is missing.
