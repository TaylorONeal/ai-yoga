"""Pull Arketa booking confirmations and reminders from Gmail.

Arketa is a yoga studio booking system used by many independent studios
(many boutique studios). Their notification emails
follow a predictable pattern that we can parse reliably.

Usage:
    python scripts/collect/gmail_arketa.py --since 2020-01-01
    python scripts/collect/gmail_arketa.py --since 2020-01-01 --out yoga_visits.xlsx
"""
from __future__ import annotations

import argparse
import base64
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

from _common import (
    DEFAULT_XLSX, get_gmail_service, load_or_create_workbook, upsert_visit
)

# Arketa's emails come from this domain
ARKETA_QUERY_BASE = "from:notifications.arketa.co"

# Reminder emails are highest-confidence (sent shortly before class)
REMINDER_SUBJECT_PATTERNS = [
    r"^Reminder - ",
    r"Your class is in 45 minutes",
]

# Reservation confirmations (lower confidence — cancellations may follow)
CONFIRMATION_SUBJECT_PATTERNS = [
    r"^Reservation Confirmation - ",
]

# Parsing patterns
CLASS_LINE = re.compile(
    r"(?P<class>[\w\s\-\(\)\&\*/']+?)\s+"
    r"(?P<teacher>[\w'\-\.]+ [\w'\.\-]+)\.?\s+"
    r"(?P<dow>Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s+"
    r"(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2}),\s+(?P<year>\d{4}),\s+"
    r"(?P<start_time>\d{1,2}:\d{2}\s*[AP]M)\s*-\s*"
    r"(?P<end_time>\d{1,2}:\d{2}\s*[AP]M)",
    re.IGNORECASE,
)
LOCATION_LINE = re.compile(r"Location:\s*(?P<address>.+)", re.IGNORECASE)


def fetch_thread_bodies(service, query: str, max_results: int = 500):
    """Yield (message_id, subject, body_text, internal_date) for matches."""
    results = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    for msg_meta in results.get("messages", []):
        msg = service.users().messages().get(
            userId="me", id=msg_meta["id"], format="full"
        ).execute()
        subject = next(
            (h["value"] for h in msg["payload"]["headers"] if h["name"] == "Subject"),
            "",
        )
        body = _extract_body(msg["payload"])
        yield msg_meta["id"], subject, body, int(msg.get("internalDate", 0))


def _extract_body(payload) -> str:
    """Walk MIME parts and return text/plain body."""
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                return base64.urlsafe_b64decode(data + "===").decode("utf-8", "ignore")
            if "parts" in part:
                inner = _extract_body(part)
                if inner:
                    return inner
        return ""
    if payload.get("mimeType") == "text/plain":
        data = payload.get("body", {}).get("data", "")
        return base64.urlsafe_b64decode(data + "===").decode("utf-8", "ignore")
    return ""


def parse_arketa_email(subject: str, body: str) -> dict | None:
    """Extract one visit dict from an Arketa email body."""
    m = CLASS_LINE.search(body)
    if not m:
        return None

    dt = datetime.strptime(
        f"{m['month']} {m['day']} {m['year']}", "%b %d %Y"
    )
    loc = LOCATION_LINE.search(body)
    location_str = loc["address"].strip() if loc else ""

    # Try to extract studio from subject or first location line
    # Arketa subjects look like "Reservation Confirmation - Class with Teacher Name"
    # Studio name is not in the subject; it usually comes from the practitioner config
    # or known mapping by location address.
    return {
        "Date": dt.date(),
        "Day": dt.strftime("%A"),
        "Time": m["start_time"].strip().upper(),
        "Style (Harmonized)": _infer_style(m["class"]),
        "Class Name (Raw)": m["class"].strip(),
        "Teacher": m["teacher"].strip(),
        "Studio": _infer_studio_from_location(location_str),
        "City": "",
        "State/Province": "",
        "Country": "",
        "Source": "Gmail (Arketa reminder)" if "Reminder" in subject else "Gmail (Arketa booking)",
        "Notes": "",
    }


STYLE_KEYWORDS = [
    ("Vinyasa (Power/Heated)", ["power vinyasa", "power", "heated"]),
    ("Vinyasa", ["vinyasa", "flow", "soul service"]),
    ("Yin / Restorative", ["yin", "restorative", "yoga nidra"]),
    ("Hatha", ["hatha"]),
    ("Kundalini", ["kundalini"]),
    ("Sculpt / Pilates", ["sculpt", "pilates"]),
    ("Workshop", ["workshop", "masterclass", "clinic"]),
    ("Retreat / Workshop", ["retreat", "immersion"]),
]


def _infer_style(class_name: str) -> str:
    name = (class_name or "").lower()
    for bucket, keywords in STYLE_KEYWORDS:
        if any(kw in name for kw in keywords):
            return bucket
    return "Other"


def _infer_studio_from_location(location_str: str) -> str:
    """Map known location strings to studio names.

    Edit this mapping for your studios. Returns the raw address as fallback.
    """
    if not location_str:
        return ""
    # Add your studio-address mappings here:
    # mapping = {
    #     "123 Main St": "Your Studio Name",
    #     "...": "Another Studio",
    # }
    return location_str


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--since", required=True, help="YYYY-MM-DD lower bound")
    p.add_argument("--out", default=str(DEFAULT_XLSX), help="Output xlsx path")
    p.add_argument(
        "--dedupe-strategy",
        choices=["stamp", "append", "skip"],
        default="stamp",
    )
    p.add_argument("--max-results", type=int, default=500)
    args = p.parse_args()

    out_path = Path(args.out)
    wb = load_or_create_workbook(out_path)
    ws = wb["Yoga Visits"]

    svc = get_gmail_service()
    since_str = args.since.replace("-", "/")
    query = f"{ARKETA_QUERY_BASE} after:{since_str}"
    print(f"Gmail query: {query}")

    counts = {"inserted": 0, "stamped": 0, "skipped": 0, "unparseable": 0}
    for msg_id, subject, body, _ in fetch_thread_bodies(svc, query, args.max_results):
        row = parse_arketa_email(subject, body)
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
