
"""Flight Schedule Parser and Query Tool."""

import sys
import os
import json
import argparse
import logging
from datetime import datetime

from validator import load_airports
from csv_loader import parse_files
from query import run_queries


STUDENT_ID = "251ADB069"
FIRST_NAME = "Remzi"
LAST_NAME = "Kutlu"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Flight Schedule Tool")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", metavar="FILE")
    group.add_argument("-d", metavar="FOLDER")
    group.add_argument("-j", metavar="FILE")

    parser.add_argument("-a", metavar="FILE")
    parser.add_argument("-o", metavar="FILE", default=None)
    parser.add_argument("-q", metavar="FILE")
    parser.add_argument("-r", metavar="FOLDER", default=".")

    args = parser.parse_args(argv)

    if (args.i or args.d) and not args.a:
        parser.error("-a is required with -i or -d")

    if args.j and args.o is not None:
        parser.error("-o cannot be used with -j")

    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)
    handler = None

    try:
        if args.j:
            with open(args.j, "r", encoding="utf-8") as file:
                db = json.load(file)

            if not isinstance(db, list):
                raise ValueError("Database must be a JSON array")

            if not all(isinstance(item, dict) for item in db):
                raise ValueError("Database must contain objects")

        else:
            if args.i:
                paths = [args.i]
            else:
                filenames = sorted(os.listdir(args.d))
                paths = []

                for name in filenames:
                    path = os.path.join(args.d, name)

                    if name.endswith(".csv") and os.path.isfile(path):
                        paths.append(path)

                if not paths:
                    raise ValueError("No CSV files found")

            airports = load_airports(args.a)

            output_path = args.o if args.o is not None else "db.json"
            log_path = os.path.join(
                os.path.dirname(os.path.abspath(output_path)),
                "errors.log"
            )

            handler = logging.FileHandler(
                log_path, mode="w", encoding="utf-8"
            )

            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))

            logger.addHandler(handler)

            db, errors = parse_files(paths, airports)

            for error in errors:
                logger.warning(error)

            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(db, file, indent=4, ensure_ascii=False)

        if args.q:
            with open(args.q, "r", encoding="utf-8") as file:
                queries = json.load(file)

            if not isinstance(queries, (dict, list)):
                raise ValueError("Queries must be a JSON object or array")

            responses = run_queries(db, queries)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M")

            filename = (
                f"response_{STUDENT_ID}_{FIRST_NAME}_"
                f"{LAST_NAME}_{timestamp}.json"
            )

            response_path = os.path.join(args.r, filename)

            with open(response_path, "w", encoding="utf-8") as file:
                json.dump(responses, file, indent=4, ensure_ascii=False)

        return 0

    except (OSError, ValueError, TypeError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())
