import csv
import os


EXPECTED_FIELDS = {"assignment", "group", "score", "weight"}
VALID_GROUPS = {"Formative", "Summative"}


def load_csv_data():
    """Ask for a CSV filename and return validated assignment records."""
    filename = input(
        "Enter the name of the CSV file to process "
        "(press Enter for grades.csv): "
    ).strip()
    if not filename:
        filename = "grades.csv"

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return None

    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty.")
        return None

    assignments = []

    try:
        with open(filename, mode="r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("Error: The CSV file does not contain a header row.")
                return None

            actual_fields = {
                field.strip().lower() for field in reader.fieldnames if field
            }
            missing_fields = EXPECTED_FIELDS - actual_fields
            if missing_fields:
                print(
                    "Error: Missing required CSV column(s): "
                    + ", ".join(sorted(missing_fields))
                )
                return None

            for row_number, row in enumerate(reader, start=2):
                if not row or all(
                    value is None or value.strip() == "" for value in row.values()
                ):
                    continue

                try:
                    assignment = row["assignment"].strip()
                    group = row["group"].strip().title()
                    score = float(row["score"])
                    weight = float(row["weight"])
                except (KeyError, TypeError, ValueError):
                    print(
                        f"Error: Row {row_number} contains missing or invalid data."
                    )
                    return None

                if not assignment:
                    print(f"Error: Row {row_number} has no assignment name.")
                    return None

                if group not in VALID_GROUPS:
                    print(
                        f"Error: Row {row_number} has invalid group '{group}'. "
                        "Use Formative or Summative."
                    )
                    return None

                if not 0 <= score <= 100:
                    print(
                        f"Error: Score for '{assignment}' must be between 0 and 100."
                    )
                    return None

                if weight <= 0:
                    print(
                        f"Error: Weight for '{assignment}' must be greater than 0."
                    )
                    return None

                assignments.append(
                    {
                        "assignment": assignment,
                        "group": group,
                        "score": score,
                        "weight": weight,
                    }
                )
    except (OSError, csv.Error) as error:
        print(f"Error: The CSV file could not be read: {error}")
        return None

    if not assignments:
        print("Error: The CSV file contains no assignment records.")
        return None

    return assignments


def evaluate_grades(data):
    """Validate weights, calculate results, and display the final decision."""
    print("\n--- Processing Grades ---")

    formative_weight = sum(
        item["weight"] for item in data if item["group"] == "Formative"
    )
    summative_weight = sum(
        item["weight"] for item in data if item["group"] == "Summative"
    )
    total_weight = formative_weight + summative_weight

    weight_errors = []
    if abs(total_weight - 100) > 0.000001:
        weight_errors.append(
            f"all assignment weights must total 100 (found {total_weight:g})"
        )
    if abs(formative_weight - 60) > 0.000001:
        weight_errors.append(
            f"Formative weights must total 60 (found {formative_weight:g})"
        )
    if abs(summative_weight - 40) > 0.000001:
        weight_errors.append(
            f"Summative weights must total 40 (found {summative_weight:g})"
        )

    if weight_errors:
        print("Weight validation failed:")
        for error in weight_errors:
            print(f"- {error}")
        return

    formative_points = sum(
        item["score"] * item["weight"] / 100
        for item in data
        if item["group"] == "Formative"
    )
    summative_points = sum(
        item["score"] * item["weight"] / 100
        for item in data
        if item["group"] == "Summative"
    )
    total_grade = formative_points + summative_points

    formative_percentage = formative_points / formative_weight * 100
    summative_percentage = summative_points / summative_weight * 100
    gpa = (total_grade / 100) * 5.0

    passed = formative_percentage >= 50 and summative_percentage >= 50

    print(f"Formative result: {formative_percentage:.2f}%")
    print(f"Summative result: {summative_percentage:.2f}%")
    print(f"Total grade: {total_grade:.2f}%")
    print(f"GPA: {gpa:.2f} / 5.00")
    print(f"Final status: {'PASSED' if passed else 'FAILED'}")

    failed_formative = [
        item
        for item in data
        if item["group"] == "Formative" and item["score"] < 50
    ]

    if not passed:
        if failed_formative:
            highest_weight = max(item["weight"] for item in failed_formative)
            resubmissions = [
                item
                for item in failed_formative
                if item["weight"] == highest_weight
            ]
            print("Eligible formative assignment(s) for resubmission:")
            for item in resubmissions:
                print(
                    f"- {item['assignment']} "
                    f"(score: {item['score']:g}%, weight: {item['weight']:g}%)"
                )
        else:
            print(
                "No failed formative assignment is eligible for resubmission."
            )


if __name__ == "__main__":
    course_data = load_csv_data()
    if course_data is not None:
        evaluate_grades(course_data)
