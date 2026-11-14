
"""Reading CSV files into flight records and error messages."""

import csv
import os

from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    records = []
    errors = []
    seen = set()

    for path in paths:
        with open(path, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)

            next(reader, None)

            for row in reader:
                line_number = reader.line_num

                if not row or all(not cell.strip() for cell in row):
                    continue

                if row[0].lstrip().startswith("#"):
                    continue

                error = validate_row(row, airports)

                if error is None:
                    record = to_record(row)
                    key = (record["flight_id"], record["departure_datetime"])

                    if key in seen:
                        error = "DUPLICATE_FLIGHT"
                    else:
                        seen.add(key)
                        records.append(record)

                if error is not None:
                    filename = os.path.basename(path)
                    original_row = ",".join(row)
                    errors.append(
                        f"{filename}:{line_number}: {error} | {original_row}"
                    )

    return records, errors
