# Collection module

Pulls class history from external sources into `yoga_visits.xlsx`. Each script targets one source and writes new rows; you run them in sequence and review the output between runs.

## Setup: Google API credentials

The Gmail and Calendar collectors use Google's official Python client and need OAuth credentials.

1. Go to https://console.cloud.google.com/, create a project (free)
2. Enable the Gmail API and Google Calendar API
3. Create OAuth 2.0 credentials (Desktop app type)
4. Download `credentials.json` and drop it in the repo root
5. First run will open a browser for consent; `token.json` is cached after

The credentials only let the scripts read your own Gmail / Calendar — they can't send or modify anything.

## Source-specific collectors

### `gmail_arketa.py`
Pulls Arketa booking confirmations. Patterns matched:
- Sender: `no-reply@notifications.arketa.co`
- Subject: `Reservation Confirmation`, `Reminder - Class with`, `Your class is in 45 minutes`

The "45 minutes" reminders are the strongest signal of attendance — the booking was active right up to class start.

### `gmail_mindbody.py`
Pulls Mindbody booking confirmations. Patterns matched:
- Sender: `*@mindbodyonline.com`, `info@*.mindbody.com`
- Subject: `Confirmation for`, `Receipt from`

Also handles the consumer schedule export from `mindbodyonline.com/explore/account/schedule` (paste the HTML and the script will parse it — see `--paste` mode).

### `gmail_walla.py`
Walla, WellnessLiving, union.fit confirmations. Generic email pattern matcher.

### `gmail_generic_booking.py`
Catchall for booking systems not specifically supported. Walks Gmail looking for "class", "reservation", "yoga" keywords + studio name list from `config/known_studios.txt`. Higher false-positive rate; expect to review each result.

### `calendar_events.py`
Walks Google Calendar for events with "yoga" in the title or matching the studio name list. Useful for catching self-organized practice (e.g., friend's Sunday Sangha, retreat blocks).

Calendar entries usually lack a teacher; the script leaves Teacher blank and flags the row for manual completion.

### `gmail_shopify_stripe.py`
Receipts from studios using e-commerce checkout (Desnudo Coffee's community flow, retail-style studios). Pattern: "Order #" + "yoga" in the line items.

### `manual_csv_import.py`
For data you'll never find in email: retreats from years ago, classes at studios that didn't use a booking system, classes paid in cash, paper class-pass cards.

Format: `templates/sample_data.csv`. The importer just appends rows; no validation against the canonical Studios list, so spell carefully.

## Dedupe rule

**Stamp existing rows; don't create parallel rows.** If the same class appears in both Arketa and the calendar, the calendar pass should detect the existing row by date + studio + teacher and just update fields (e.g., add the Calendar source tag), not create a second row.

Each collector has a `--dedupe-strategy` flag:
- `stamp` (default): update existing rows in place
- `append`: add as new row, leave dedupe to a later pass
- `skip`: only add rows that have no date+studio match

When in doubt: `--dedupe-strategy stamp`.

## Source tag conventions

Column 11 (Source) should encode where the row came from. Standard tags:

| Tag | Meaning |
|-----|---------|
| `Gmail (Arketa booking)` | Arketa booking confirmation |
| `Gmail (Arketa reminder)` | Arketa 45-min reminder (highest confidence) |
| `Gmail (Mindbody)` | Mindbody confirmation |
| `Gmail (Shopify)` | Shopify-style receipt |
| `Calendar` | Google Calendar entry |
| `Mindbody schedule (browser)` | Consumer schedule export |
| `Manual` | Hand-entered |
| `Swarm` | Foursquare/Swarm check-in (cross-reference only) |

Multiple sources can be joined with ` + ` like teacher names: `Gmail (Arketa) + Calendar`.

## Review checklist after each run

1. Sort by Date and scan the new rows
2. Check Day-of-week — if a class shows the wrong day, it's a timezone issue at the collector
3. Check Teacher field for `None` / empty strings; usually means the collector couldn't parse the booking
4. Check the Studio column for misspellings or new variants (then update `config/known_studios.txt`)
5. Spot-check 3-5 rows against the source email to make sure the parser isn't drifting
