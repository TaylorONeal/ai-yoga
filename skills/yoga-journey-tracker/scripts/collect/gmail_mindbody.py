"""Pull Mindbody booking confirmations from Gmail.

Mindbody powers thousands of yoga, fitness, and wellness studios. Their
confirmation emails are sent from per-studio addresses but follow a
consistent template.

Usage:
    python scripts/collect/gmail_mindbody.py --since 2020-01-01
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from _common import (
    DEFAULT_XLSX, get_gmail_service, load_or_create_workbook, upsert_visit
)
from gmail_arketa import fetch_thread_bodies, _infer_style

MINDBODY_QUERY_BASE = "from:mindbodyonline.com OR from:*.mindbody.com"

CLASS_PATTERN = re.compile(
    r"(?P<class>[\w\s\-\(\)\&/']+?)\s+(?:with|w/)\s+(?P<teacher>[\w'\-\.]+(?:\s[\w'\-\.]+)?)",
    re.IGNORECASE,
)
DATE_TIME_PATTERN = re.compile(
    r"(?P<dow>Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,?\s+"
    r"(?P<month>[A-Z][a-z]+)\s+(?P<day>\d{1,2})(?:,\s*(?P<year>\d{4}))?\s+"
    r"at\s+(?P<time>\d{1,2}:\d{2}\s*[AP]M)",
    re.IGNORECASE,
)
STUDIO_PATTERN = re.compile(
    r"(?:located at|at)\s+(?P<studio>[\w\s\-&']+?)(?:\.|,|\n)",
    re.IGNORECASE,
)


def parse_mindbody_email(subject: str, body: str) -> dict | None:
    class_m = CLASS_PATTERN.search(body)
    dt_m = DATE_TIME_PATTERN.search(body)
    studio_m = STUDIO_PATTERN.search(body)
    if not (class_m and dt_m):
        return None

    year = dt_m.group("year") or str(datetime.now().year)
    try:
        dt = datetime.strptime(
            f"{dt_m['month']} {dt_m['day']} {year}", "%B %d %Y"
        )
    except ValueError:
        try:
            dt = datetime.strptime(
                f"{dt_m['month']} {dt_m['day']} {year}", "%b %d %Y"
            )
        except ValueError:
            return None

    return {
        "Date": dt.date(),
        "Day": dt.strftime("%A"),
        "Time": dt_m["time"].strip().upper(),
        "Style (Harmonized)": _infer_style(class_m["class"]),
        "Class Name (Raw)": class_m["class"].strip(),
        "Teacher": class_m["teacher"].strip(),
        "Studio": (studio_m["studio"].strip() if studio_m else ""),
        "City": "",
        "State/Province": "",
        "Country": "",
        "Source": "Gmail (Mindbody)",
        "Notes": "",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--since", required=True)
    p.add_argument("--out", default=str(DEFAULT_XLSX))
    p.add_argument(
        "--dedupe-strategy",
        choices=["stamp", "append", "skip"],
        default="stamp",
    )
    p.add_argument("--max-results", type=int, default=1000)
    args = p.parse_args()

    out_path = Path(args.out)
    wb = load_or_create_workbook(out_path)
    ws = wb["Yoga Visits"]

    svc = get_gmail_service()
    since_str = args.since.replace("-", "/")
    query = f"({MINDBODY_QUERY_BASE}) after:{since_str}"
    print(f"Gmail query: {query}")

    counts = {"inserted": 0, "stamped": 0, "skipped": 0, "unparseable": 0}
    for msg_id, subject, body, _ in fetch_thread_bodies(svc, query, args.max_results):
        row = parse_mindbody_email(subject, body)
        if not row:
            counts["unparseable"] += 1
            continue
        outcome = upsert_visit(ws, row, args.dedupe_strategy)
        counts[outcome] = counts.get(outcome, 0) + 1

    wb.save(out_path)
    print(f"Results: {counts}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
