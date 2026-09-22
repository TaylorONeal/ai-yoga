---
name: yoga-journey-tracker
description: Compile, reconcile, and explore a personal yoga practice history from booking records, studio exports, calendars, and memory. Covers Momence, Mindbody, Arketa, Walla, and other sources while keeping attendance, multi-class days, training hours, and uncertain records distinct. Use to build or update a practice log, retrospective, dashboard, or teacher history.
license: MIT
---

# Yoga Journey Tracker

Build a history the practitioner can trust, not just a large count. Recover scattered evidence, reconcile it into a private ledger, then help them see teachers, places, rhythms, and learning across time. The raw ledger, analytical totals, and public presentation are different artifacts.

## Choose the job

- **First compile:** inventory sources and existing spreadsheets, then collect in bounded batches.
- **Update:** start from the existing canonical ledger and process the uncovered period; do not rebuild from zero.
- **Reconcile:** compare a studio export or user correction with earlier inferences while preserving audit history.
- **Explore or present:** use a reconciled dataset; state attendance filters and denominators before writing a story or chart.

Ask once for missing essentials: the private ledger location, date range, available accounts/exports, and whether the scope includes workshops, retreats, personal practice, and classes taught. Reuse existing answers. Do not assume the user's home country, studio, teaching status, or training history.

## Read the relevant method

- Before collection: [booking-source field guide](references/booking-sources.md), including Momence, old/new Arketa senders, Mindbody completed visits, Walla, WellnessLiving, union.fit, FitGrid, LoyalSnap, Gymdesk, retreat.guru, payment/event receipts, direct studios, calendars, legacy mailboxes and manual evidence.
- Before any merge, correction or totals: [reconciliation rules](references/reconciliation.md).
- Before scripting: [collection scripts and limits](scripts/collect/README.md) and [schema](config/schema.json). Inspect an existing workbook's actual columns/sheets first.

## 1. Collect without flattening the evidence

Pair booking-platform history with direct studio correspondence, authorized calendars, legacy mailboxes, and user-supplied attendance exports. Search each source across the requested years with complete pagination; record coverage and failures. A source returning no records means no records found within that search, not no practice.

Momence is a first-class source: inspect booking, receipt, cancellation and post-class messages, plus any user-provided attendance export. Preserve occurrence, attendee, venue, local time and status. The field guide provides search leads; do not pretend this repository ships a Momence API connector.

Retain raw labels and source IDs privately. Stage candidates and parse failures before changing the ledger. Bookings, reminders, payment receipts and class-pack purchases are not interchangeable. A reminder does not prove attendance. Match cancellations to the same attendee and occurrence; a guest alias cancellation must not cancel the user's separate booking.

## 2. Reconcile conservatively

The visit unit is one class occurrence for one practitioner. Prefer provider IDs; otherwise compare location + local date + time + class + teacher. Do not collapse two legitimate classes at one studio on one day. Unknown time or teacher is unresolved matching evidence, not permission to merge.

Use confirmed, provisional, excluded and unresolved states in the audit. In the existing workbook, preserve `Unsure Attended`, `Check-in Confirmed`, source and notes fields; do not interpret an empty uncertainty cell as check-in proof. Specific user-confirmed recollection is valid evidence with its own provenance. Unknown dates stay in a review queue rather than acquiring invented exact dates.

A studio attendance export can correct inferred visits within its coverage. Stage the diff, preserve annotations and out-of-range history, and version the workbook before replacement. Never delete every row for a studio merely to import a partial export.

Normalize teacher aliases only with identity evidence. Keep co-teachers distinct, raw class names intact, studio locations separate from brands, and rebrands searchable. Convert classes to the studio's local timezone with provenance, not the practitioner's home zone.

## 3. Analyze with explicit definitions

Report event count and distinct practice-day count separately. Count co-teachers individually. Separate completed formal training hours, in-progress programs, workshops with evidenced durations, retreat sessions, and classes taught. A timetable is not a record that every offered session was attended; a YTT-tagged class is not a completed credential.

Use confirmed-only totals by default for attendance claims and show provisional/unresolved counts alongside them. If the user chooses a wider definition, label it clearly throughout the dashboard and narrative. Do not turn missing-source years into a story about motivation. Use user-selected home-country context for international comparisons, not a hardcoded country.

## 4. Produce a useful view

For a first result, deliver the ledger update and a compact review: covered dates/sources, confirmed visits, distinct days, provisional records, new/merged rows, and unresolved decisions. Then, if requested, create an HTML dashboard, slides, or teacher document from that reviewed data using available document tools.

A good retrospective can include yearly/monthly rhythm, style mix, teachers and studios, places, training milestones, and meaningful turning points grounded in the user's own account. Every chart needs units and population. Apply public-export name overrides only at the presentation layer. Do not publish exact personal movement history by default.

Output-rendering scripts are not currently included in this package. Generate those artifacts with the assistant's available tools when requested; do not run nonexistent `scripts/output/*` commands or promise a one-command deck builder.

## Included helpers and safe use

The manual CSV importer and legacy Arketa/Mindbody/calendar collectors exist. The collectors need credential setup and representative template review; coverage is narrower than the assisted field guide. Run imports on a private staged copy first. Use the assistant's real supported account connection if available, otherwise accept user-provided exports. Never invent API methods or request credentials in a prompt.

The canonical workbook has 19 visit columns plus optional Studios, Instructors, Planned_Trainings, Teaching_Log and Summary sheets; see `config/schema.json`. Preserve unrelated sheets and formulas. Keep credentials, tokens, raw exports, evidence sidecars, workbook versions, practitioner config and generated outputs outside this public repository.

## Completion checks

Reconcile counts before/after, inspect suspected duplicate groups and cancellation cases, and verify that re-import does not inflate visits. Keep multiple same-day sessions, unknown-date records and uncertainty visible. Confirm source coverage and chart denominators. A successful script exit is not proof that the historical interpretation is correct.
