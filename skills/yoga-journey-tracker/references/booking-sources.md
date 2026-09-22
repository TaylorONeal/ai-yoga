# Booking-source field guide

Use this when gathering practice history. These are search leads learned from real collection work, not guarantees of current vendor behavior or claims that an API integration ships here. Verify the actual sender and template in the user's mailbox. Search domains first, then subjects, then studio names. Group OR terms so an unrelated “confirmation” search does not escape the sender filter. Use the connected tool's documented query syntax; examples below are Gmail search expressions.

| Source | Discovery query / material | Extract and reconcile |
| --- | --- | --- |
| **Momence** | `from:momence.com {booking confirmation receipt "You're in" "what did you think" cancel}`; inspect `momence@mail.momence.com` when present | Class occurrence, venue, teacher, attendee, reservation ID, status and timezone. A receipt can purchase a pack. Pair cancellations with that booking/attendee, and treat feedback requests as corroboration, not attendance proof. Use a user-provided attendance export when available. |
| Arketa, current and older | `{from:notifications.arketa.co from:reservations@arketa.co}` | Confirmation plus 24-hour and 45-minute reminders may be three records of one class. Preserve address and class start time; do not use the email arrival date as class date. Search both sender generations. |
| Mindbody | `from:mindbodyonline.com {receipt reservation confirmation reminder "Thank You for Visiting"}` | Purchases, bookings, completed visits and welcome emails have different meanings. Studio business-number senders may reveal old history. Consumer completed-visit history or a studio export can fill missing email records. |
| Walla | `from:hellowalla.com {booked reminder cancel}` | Separate automation from newsletters. Extract class, teacher, date, time and location. |
| WellnessLiving | `from:wellnessliving.com {booked reminder cancel}` | Personalized subject lines can include the user's first name; inspect the body rather than assuming every message is a visit. |
| union.fit | `from:union.fit {receipt registration canceled cancelled}` | An order may contain several registrations. Reconcile each occurrence and cancellation. |
| FitGrid | `{from:fitgrid.com from:followup.fitgrid.com}` | Follow-ups can supply teacher and studio names absent from a booking; automation is supporting evidence, not guaranteed check-in. |
| LoyalSnap | `from:loyalsnap.com {first welcome class}` | Separate post-visit language from sales campaigns. |
| Gymdesk | `from:gymdesk.com {booking reminder cancel}` | Sender subdomains may identify the studio. Verify location and local start time. |
| retreat.guru | `from:retreat.guru` plus the organizer's domain | Program dates, registration, schedules, orientation, cancellation, and thank-you messages. Registration is not a row for every possible session. |
| Stripe, PayPal, Square, Shopify | Sender/domain plus a known studio or yoga-related line item | Distinguish drop-in, deposit, balance, membership, retail and class-pack purchases. Payment supports a transaction, not a count of attended classes. |
| Eventbrite, Wix Events, Book4Time | Event confirmation/history plus the actual organizer | Separate ticket, attendance, cancellation, spa treatment and yoga component. |
| Direct studio correspondence | Studio domains, organizer threads, attached or photographed schedules | Historical teacher rosters and program changes. A printed schedule shows what was offered, not what the user attended. |
| Calendar | Search authorized calendars by year; paginate and expand recurrence correctly | Accepted plans, declined/optional events, classes taught, personal practice, reminders, travel conflicts. An event title containing “yoga” is not enough. |
| Legacy mailbox / export | User-provided archives, studio exports, booking-history files | Older accounts can contain whole eras absent from the current inbox. Record coverage dates rather than treating a missing era as no practice. |
| Manual memory, notebooks, check-ins | Specific dates and recollections, photos, optional location/check-in exports | Keep provenance and uncertainty. A venue check-in may support a visit but not identify a particular class. |

## Collection procedure

1. Agree on account scope, time range, practice categories, and private output location. Use available authorized access; never invent a connector or ask for a password in chat.
2. Inventory sources and date coverage before searching. Work in bounded year/provider batches. Follow all page tokens. Record query, coverage, result count, and unresolved parsing cases.
3. Read class details, not just subject lines. Keep source record ID, provider booking ID when available, attendee identity, local date/time, original timezone, raw class/teacher/studio text, and observed status in private evidence records.
4. Search cancellation and reschedule messages for the same occurrence and attendee. A guest booking sent to a plus-address alias must not cancel the primary attendee's separate booking.
5. Stage candidates, parse failures, and non-class transactions separately. Do not silently discard difficult records or publish raw messages.
6. Reconcile against existing rows before import, then run the checks in [reconciliation.md](reconciliation.md).

## Retreat enrichment

Read pre-trip schedules, orientation messages, daily changes, post-trip notes, and the user's recollection together. A weekly timetable is evidence of an offered session, not attendance on every matching weekday. Keep program days, yoga sessions, non-asana training blocks, and certified training hours distinct. Default to the recalled/session-evidenced count. Expand to all offered sessions only with explicit confirmation, and retain what supports the expansion.

## What ships

The repository contains manual CSV import and legacy Gmail Arketa/Mindbody and calendar collector scripts. The latter require provider credentials and template review; they are not universal parsers. Momence and the other providers above are supported as an assisted search/export workflow, not a fabricated one-command API integration. Normalize a reviewed export into the canonical CSV schema and import it with the supplied importer.
