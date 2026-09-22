"""Summarize a reviewed workbook with explicit attendance and hour definitions.

Usage: python scripts/analyze/aggregate_stats.py --input visits.xlsx --output stats.json
Optional: --include-provisional (clearly labelled wider population)
"""
from __future__ import annotations
import argparse
import json
import math
from collections import Counter
from datetime import date, datetime
from pathlib import Path
import openpyxl
import yaml

ROOT = Path(__file__).resolve().parents[2]


def to_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%B %d, %Y"):
        try:
            return datetime.strptime(str(value), fmt).date()
        except ValueError:
            pass
    return None


def attendance(row):
    """Use structured flags/status, never guess attendance from a blank cell."""
    yes = {"y", "yes", "true", "1"}
    state = str(row.get("Attendance Status", "")).strip().casefold()
    if state in {"cancelled", "canceled", "late cancel", "late-canceled", "absent", "no show", "no-show", "excluded"}:
        return "excluded"
    if str(row.get("Unsure Attended") or "").strip().casefold() not in {"", "n", "no", "false", "0"}:
        return "provisional"
    if state in {"confirmed", "attended", "signed in", "user-confirmed"} or str(row.get("Check-in Confirmed", "")).strip().casefold() in yes:
        return "confirmed"
    return "provisional"


def load_rows(ws):
    headers = [cell.value for cell in ws[1]]
    result = []
    for values in ws.iter_rows(min_row=2, values_only=True):
        if not any(value is not None for value in values):
            continue
        row = dict(zip(headers, values))
        row["date"] = to_date(row.get("Date"))
        row["attendance"] = attendance(row)
        result.append(row)
    return result


def verified_hours(entries):
    """Only sum explicit nonnegative finite hours; unknown remains unknown."""
    values = [e.get("hours") for e in entries]
    valid = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v >= 0]
    return {"known_hours": sum(valid), "entries_with_hours": len(valid), "entries_without_hours": len(entries) - len(valid)}


def summarize(rows, config=None, include_provisional=False):
    config = config or {}
    states = Counter(row["attendance"] for row in rows)
    chosen = [row for row in rows if row["date"] and (row["attendance"] == "confirmed" or (include_provisional and row["attendance"] == "provisional"))]
    teachers = Counter()
    for row in chosen:
        teachers.update(set(t.strip() for t in str(row.get("Teacher") or "").split(" + ") if t.strip()))
    years = Counter(row["date"].year for row in chosen)
    months = Counter(row["date"].strftime("%Y-%m") for row in chosen)
    days = {row["date"] for row in chosen}
    def counts(column):
        return Counter(str(row.get(column) or "Unknown") for row in chosen)
    def records(counter, key):
        return [{key: label, "count": count} for label, count in counter.most_common()]
    studios = counts("Studio")
    countries = counts("Country")
    first = min(days) if days else None
    last = max(days) if days else None
    duration = (last - first).days + 1 if first else 0
    completed = [entry for entry in config.get("featured_trainings", []) if entry.get("status") == "completed"]
    return {
        "population": "confirmed + provisional" if include_provisional else "confirmed only",
        "definitions": {
            "visit": "one included class occurrence; input must be reconciled before aggregation",
            "practice_day": "one distinct local date with an included visit",
            "teacher": "individual co-teachers counted separately; aliases must be reviewed first",
            "training": "hours come only from explicit configuration, never inferred from visit tags",
        },
        "records_reviewed": len(rows),
        "attendance_counts": {key: states[key] for key in ("confirmed", "provisional", "excluded")},
        "undated_records": sum(row["date"] is None for row in rows),
        "total_visits": len(chosen), "practice_days": len(days),
        "first_date": str(first) if first else None, "last_date": str(last) if last else None,
        "visits_per_week_observed_span": round(len(chosen) * 7 / duration, 2) if duration >= 7 else None,
        "unique_teachers": len(teachers),
        "unique_studios": len([s for s in studios if s != "Unknown"]),
        "unique_countries": len([c for c in countries if c != "Unknown"]),
        "yearly": [{"year": y, "count": years[y]} for y in sorted(years)],
        "monthly": [{"month": m, "count": months[m]} for m in sorted(months)],
        "top_teachers": records(teachers, "teacher"),
        "top_studios": records(studios, "studio"),
        "countries": records(countries, "country"),
        "styles": records(counts("Style (Harmonized)"), "style"),
        "training_hours": {
            "completed_formal": verified_hours(completed),
            "in_progress": verified_hours(config.get("in_progress_trainings", [])),
            "workshops": verified_hours(config.get("workshops", [])),
        },
        "warnings": ["Counts depend on prior identity/status reconciliation; booking and calendar records remain provisional unless confirmed.",
                     "Unspecified training/workshop hours are unknown, not zero or estimated credentials."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ROOT / "yoga_visits.xlsx"))
    parser.add_argument("--output", default=str(ROOT / "stats.json"))
    parser.add_argument("--config", help="Private practitioner YAML with explicit training hours")
    parser.add_argument("--include-provisional", action="store_true")
    args = parser.parse_args()
    config = yaml.safe_load(Path(args.config).read_text()) or {} if args.config else {}
    workbook = openpyxl.load_workbook(args.input, data_only=True)
    data = summarize(load_rows(workbook["Yoga Visits"]), config, args.include_provisional)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {output}: {data['total_visits']} visits / {data['practice_days']} practice days ({data['population']})")


if __name__ == "__main__":
    main()
