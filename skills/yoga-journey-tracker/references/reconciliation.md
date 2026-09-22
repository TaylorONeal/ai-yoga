# Reconcile a practice history

## Preserve evidence and identity

One class occurrence for one practitioner is the unit of a visit. Neither one email nor one day is that unit. Prefer a provider occurrence/booking ID plus attendee when available. Otherwise compare studio/location, local date, start time, class, and teacher. Same date and studio alone can collapse a real double-class day. A missing time is uncertainty, not a wildcard allowing automatic merge.

For each candidate keep raw labels, normalized labels, source IDs and status separately. The 19-column workbook is the human-facing ledger; private sidecar evidence may carry richer IDs and status history without forcing a destructive schema migration. Do not overwrite user annotations while enriching a row.

## Attendance is a decision with evidence

| Evidence | Treatment |
| --- | --- |
| Explicit current correction by practitioner | Apply it; preserve the replaced inference in the audit |
| Attendance/check-in export with clear per-class status | Strong occurrence evidence within the export's coverage |
| Specific, affirmative personal recollection | User-confirmed, with that provenance; do not pretend it is electronically verified |
| Booking plus reminder or generic post-class email | Provisional unless attendance is established elsewhere |
| Canceled, late-canceled, absent, no-show | Exclude from attended totals; retain the evidence and booking history |
| Unclear or conflicting status | Unresolved; do not silently count or delete |
| Membership, class pack, retail, deposit | Transaction evidence, not an attended session |
| Calendar slot, optional recurring invitation | Planned unless confirmed; declined/unanswered is not attended |
| Class taught | Separate teaching log unless the user explicitly defines another scope |

Do not assume that no reminder means absence. Do not assume that a 45-minute reminder or feedback email proves arrival. Do not infer attendance from a travel gap alone.

## Reconcile an authoritative studio export

Inspect the export's dates, studio locations, attendee, and status definitions first. Stage a row-level comparison: exact matches, new visits, contradicted inferences, unmatched prior visits, and ambiguous cases. Update only the covered interval and matched identity. Preserve older/manual evidence outside coverage. A portal export is not permission to delete every row for that studio. Save a versioned backup and report before/after counts before applying replacements.

For Momence or any other export, do not assume a universal status vocabulary. Map the actual exported statuses to confirmed/provisional/excluded and show the mapping. Keep declined bookings available for reconciliation while excluding them from attended counts.

## Names and places

Keep raw class names even when style buckets are normalized. Teacher aliases require evidence that they are the same person; a shared surname is insufficient. Co-teachers are distinct individuals and one co-taught class is still one visit. Preserve accents and legitimate name changes; do not guess gender or impose a married-name convention.

A studio brand is not a venue: same-name locations in different cities remain distinct. Rebrands may share a stable venue identity if evidence supports continuity; relocations need distinct location history. Keep historical names searchable, and do not erase a closed studio from past practice. Use the existing country/style schema consistently rather than mixing full names and abbreviations halfway through a workbook.

## Time and scope

Use studio-local class date/time and record timezone provenance. Email sent time is not class start time. Treat DST, overnight travel, and calendar conversions explicitly. Preserve all-day retreats as program blocks until actual sessions are established; do not invent an 08:00 class.

Separate: visits (events), distinct practice days, yoga sessions within retreats, formal completed training hours, in-progress training, workshops, and classes taught. Never infer a 200-hour credential from one row tagged YTT or multiply program hours by session count. Avoid converting all workshops to a standard guessed duration. Mark estimates as estimates, with a visible denominator.

## Output and audit

Maintain confirmed, provisional, excluded and unresolved counts. Chart titles must state the included population. A teacher list counts individuals rather than “Teacher A + Teacher B” as one person. A streak uses distinct local practice days, not number of sessions. Show source coverage gaps rather than explaining them as a lapse in commitment.

Checks before saving:

- Row count change reconciles to added/merged/reclassified records.
- Re-import of the same reviewed data does not add visits.
- Same-day sessions survive when their times/classes differ.
- Unknown-date records remain in a review queue, not assigned today's date.
- Cancellations match the correct attendee and occurrence.
- Raw evidence, user notes, and records outside an export's coverage survive.
- Figures and narrative agree with the chosen attendance filter.
- Display-only anonymization affects exports, never source identities.

A public dashboard gets only the user-approved aggregate subset. Private names, source IDs, emails, credentials, and exact movement history do not belong in the skill repository or a sample dataset.
