"""Import manual visits from a CSV file.

For classes that never made it into email or calendar — old retreats,
cash-paid classes, pre-digital studio cards, classes you remember but
can't verify electronically.

CSV format: see templates/sample_data.csv

Usage:
    python scripts/collect/manual_csv_import.py my_history.csv
    python scripts/collect/manual_csv_import.py my_history.csv --out yoga_visits.xlsx
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

from _common import (
    COLUMNS, DEFAULT_XLSX, load_or_create_workbook, upsert_visit, to_date
)


def parse_csv_row(row: dict) -> dict | None:
    d = to_date(row.get("Date") or row.get("date"))
    if not d:
        return None

    out = {col: row.get(col) for col in COLUMNS if col in row}
    out["Date"] = d
    out["Day"] = out.get("Day") or d.strftime("%A")
    out["Source"] = out.get("Source") or "Manual"
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_path", help="Input CSV (see templates/sample_data.csv)")
    p.add_argument("--out", default=str(DEFAULT_XLSX))
    p.add_argument(
        "--dedupe-strategy",
        choices=["stamp", "append", "skip"],
        default="stamp",
    )
    args = p.parse_args()

    out_path = Path(args.out)
    wb = load_or_create_workbook(out_path)
    ws = wb["Yoga Visits"]

    counts = {"inserted": 0, "stamped": 0, "skipped": 0, "unparseable": 0}
    with open(args.csv_path, encoding="utf-8-sig") as f:
        for csv_row in csv.DictReader(f):
            row = parse_csv_row(csv_row)
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
