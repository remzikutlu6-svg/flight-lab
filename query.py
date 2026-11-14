
"""Running queries against the flight database."""

from datetime import datetime
import math


RECORD_KEYS = [
    "flight_id", "origin", "destination",
    "departure_datetime", "arrival_datetime", "price"
]

ALLOWED_KEYS = RECORD_KEYS + [
    "min_price", "sort_by", "order", "limit"
]


def valid_date(value):
    if not isinstance(value, str):
        return False

    try:
        date = datetime.strptime(value, "%Y-%m-%d %H:%M")
        return date.strftime("%Y-%m-%d %H:%M") == value
    except ValueError:
        return False


def run_query(db: list[dict], query: dict) -> dict:
    if not isinstance(query, dict):
        return {
            "query": query,
            "error": "INVALID_QUERY",
            "matches": []
        }

    for key, value in query.items():
        if key not in ALLOWED_KEYS:
            return {
                "query": query,
                "error": "INVALID_QUERY",
                "matches": []
            }

        if key in ["flight_id", "origin", "destination"]:
            if not isinstance(value, str):
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

        elif key in ["departure_datetime", "arrival_datetime"]:
            if not valid_date(value):
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

        elif key in ["price", "min_price"]:
            if (isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(value)):
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

        elif key == "sort_by":
            if value not in RECORD_KEYS:
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

        elif key == "order":
            if value not in ["asc", "desc"]:
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

        elif key == "limit":
            if type(value) is not int or value < 0:
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

    if "order" in query and "sort_by" not in query:
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = []

    for flight in db:
        if "flight_id" in query and flight["flight_id"] != query["flight_id"]:
            continue

        if "origin" in query and flight["origin"] != query["origin"]:
            continue

        if "destination" in query and flight["destination"] != query["destination"]:
            continue

        if ("departure_datetime" in query
                and flight["departure_datetime"] < query["departure_datetime"]):
            continue

        if ("arrival_datetime" in query
                and flight["arrival_datetime"] > query["arrival_datetime"]):
            continue

        if "price" in query and flight["price"] > query["price"]:
            continue

        if "min_price" in query and flight["price"] < query["min_price"]:
            continue

        matches.append(flight)

    if "sort_by" in query:
        sort_key = query["sort_by"]
        descending = query.get("order", "asc") == "desc"

        matches = sorted(
            matches,
            key=lambda flight: flight[sort_key],
            reverse=descending
        )

    if "limit" in query:
        matches = matches[:query["limit"]]

    return {"query": query, "matches": matches}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    if isinstance(queries, dict):
        queries = [queries]

    return [run_query(db, query) for query in queries]
