# Collection scripts

Read the [booking-source guide](../../references/booking-sources.md) and [reconciliation method](../../references/reconciliation.md) before collection.

Implemented helpers:

- `manual_csv_import.py`: reviewed rows in the 19-column canonical CSV format → workbook. Supports `--out` and `--dedupe-strategy stamp|append|skip`.
- `gmail_arketa.py`: legacy template parser for Arketa messages; inspect the actual email format and review output.
- `gmail_mindbody.py`: legacy template parser for Mindbody; inspect the implementation rather than assuming HTML/browser-export support.
- `calendar_events.py`: legacy Google Calendar collector; plans require attendance reconciliation.
- `_common.py`: workbook and read-only Google API helpers.

Momence, Walla, WellnessLiving and the other sources in the guide have an assisted search/export method, not dedicated scripts here. The scripts formerly listed as `gmail_walla.py`, `gmail_generic_booking.py`, and `gmail_shopify_stripe.py` do not ship. Do not call them.

For an export from any platform, inspect columns/statuses, normalize reviewed records to `templates/sample_data.csv`, then import into a staged workbook. Preserve raw export and provenance privately. Review matches before replacing a canonical workbook.

Google collectors require the packages in `requirements.txt`, a user-configured Google Cloud desktop OAuth client, enabled APIs, and read-only authorization. Never publish `credentials.json`, `token_gmail.json`, or `token_calendar.json`. No live-account test or credential setup is implied by installing this skill.

The included legacy collectors are partial helpers, not exhaustive evidence pipelines. Use bounded queries and verify all pages were retrieved. Template drift, missing HTML handling, unparsed records, and status reconciliation need explicit review. Booking/reminder/calendar output must remain provisional until attendance is established.
