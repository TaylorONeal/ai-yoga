"""Pull Google Calendar events that look like yoga.

Catches self-organized practice (Sunday Sangha, friend's class, retreat
blocks) and serves as a cross-reference for emails that may have been
missed.

Usage:
    python scripts/collect/calendar_events.py --since 2020-01-01
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from _common import (
    DEFAULT_XLSX, get_calendar_service, load_or_create_workbook, upsert_visit
)
from gmail_arketa import _infer_style

YOGA_KEYWORDS = [
    "yoga", "vinyasa", "flow", "hatha", "ashtanga", "yin", "restorative",
    "kundalini", "sangha", "sadhana", "meditation", "retreat", "workshop",
]


def looks_like_yoga(event: dict) -> bool:
    text = " ".join(
        str(event.get(k, "") or "") for k in ("summary", "description", "location")
    ).lower()
    return any(kw in text for kw in YOGA_KEYWORDS)


def event_to_row(event: dict) -> dict | None:
    start = event.get("start", {})
    start_iso = start.get("dateTime") or start.get("date")
    if not start_iso:
        return None
    if "T" in start_iso:
        dt = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    else:
        dt = datetime.fromisoformat(start_iso + "T00:00:00+00:00")

    summary = event.get("summary", "")
    location = event.get("location", "")

    return {
        "Date": dt.date(),
        "Day": dt.strftime("%A"),
        "Time": dt.strftime("%I:%M %p") if "T" in start_iso else "",
        "Style (Harmonized)": _infer_style(summary),
        "Class Name (Raw)": summary,
        "Teacher": "",
        "Studio": location.split(",")[0].strip() if location else "",
        "City": "",
        "State/Province": "",
        "Country": "",
        "Source": "Calendar",
        "Notes": (event.get("description", "") or "")[:240],
        "Unsure Attended": "Y",  # Calendar entry alone isn't proof of attendance
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--since", required=True)
    p.add_argument("--out", default=str(DEFAULT_XLSX))
    p.add_argument("--calendar-id", default="primary")
    p.add_argument(
        "--dedupe-strategy",
        choices=["stamp", "append", "skip"],
        default="stamp",
    )
    p.add_argument("--max-results", type=int, default=2500)
    args = p.parse_args()

    out_path = Path(args.out)
    wb = load_or_create_workbook(out_path)
    ws = wb["Yoga Visits"]

    svc = get_calendar_service()
    time_min = f"{args.since}T00:00:00Z"
    time_max = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    counts = {"inserted": 0, "stamped": 0, "skipped": 0, "filtered": 0}
    page_token = None
    fetched = 0
    while True:
        resp = svc.events().list(
            calendarId=args.calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=250,
            singleEvents=True,
            orderBy="startTime",
            pageToken=page_token,
        ).execute()
        for ev in resp.get("items", []):
            fetched += 1
            if not looks_like_yoga(ev):
                counts["filtered"] += 1
                continue
            row = event_to_row(ev)
            if not row:
                continue
            outcome = upsert_visit(ws, row, args.dedupe_strategy)
            counts[outcome] = counts.get(outcome, 0) + 1
            if fetched >= args.max_results:
                break
        page_token = resp.get("nextPageToken")
        if not page_token or fetched >= args.max_results:
            break

    wb.save(out_path)
    print(f"Fetched {fetched} events. Results: {counts}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
