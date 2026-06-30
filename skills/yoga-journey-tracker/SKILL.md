---
name: yoga-journey-tracker
description: Build, maintain, and visualize a personal yoga practice log — every class, retreat, training, and workshop across years and continents. Use when the user asks to track their yoga practice, compile a yoga visits log, count classes attended, build a yoga dashboard, generate a yoga journey presentation, audit yoga teachers and studios, or pull yoga bookings from Gmail/Calendar/Mindbody/Arketa/Walla. Three-module architecture: collection (pull from booking systems, calendar, email, manual entry), analysis (aggregate stats, harmonize teacher names, classify training hours), and output (PowerPoint deck, HTML dashboard, teachers Word doc). Works for any practitioner, any style, any duration of practice. Also trigger when someone says "where have I been practicing," "how many classes have I taken," "build me a yoga retrospective," or "I want to see my yoga history visualized."
license: MIT
---

# Yoga Journey Tracker

A reproducible system for collecting, analyzing, and visualizing a personal yoga practice log. Built from real-world experience compiling a multi-year practice log spanning dozens of studios, hundreds of teachers, and many countries.

## What this skill does

Takes a practitioner's class history from messy sources (Gmail booking confirmations, calendar events, Mindbody/Arketa schedules, manual notes) and turns it into a clean spreadsheet, then renders that spreadsheet as a dashboard and presentation. Designed for the kind of person who has been practicing for years across multiple studios and wants to actually see their journey.

## Three modules

The work splits cleanly into three phases. Run them in order on a fresh dataset, then re-run collection and rebuild outputs whenever you want a refresh.

```
1. Collection & Storage  →  yoga_visits.xlsx (canonical store)
2. Analysis              →  aggregated_stats.json
3. Output Creation       →  deck.pptx + dashboard.html + teachers.docx
```

Each module has its own folder under `scripts/` with focused, single-purpose scripts. Read the module README for details when you start working in that phase.

### Module 1: Collection & Storage

**Goal:** populate `yoga_visits.xlsx` with one row per class attended.

**Read first:** `scripts/collect/README.md` for the 19-column schema and harmonization rules.

**Sources supported out of the box:**
- Gmail booking confirmations (Arketa, Mindbody, Walla, WellnessLiving, union.fit, retreat.guru)
- Google Calendar events
- Shopify / Stripe receipts (for studios using e-commerce checkout)
- Manual CSV import (for retreats, workshops, classes without electronic records)
- Eventbrite confirmations
- Foursquare/Swarm check-ins (for cross-referencing dates)

**Run order on a fresh dataset:**
1. `python scripts/collect/manual_csv_import.py templates/sample_data.csv` to seed structure
2. `python scripts/collect/gmail_arketa.py --since 2020-01-01` for one booking system at a time
3. `python scripts/collect/calendar_events.py --since 2020-01-01` to catch self-organized entries
4. Manually review and dedupe; the dedupe rule is **stamp existing rows with new metadata, don't create parallel rows** for the same class

### Module 2: Analysis

**Goal:** produce a stats bundle that downstream rendering scripts can consume.

**Read first:** `scripts/analyze/README.md` for the harmonization patterns and the training-vs-workshop-vs-retreat split.

**Key operations:**
- **Aggregate** per year, per month, per studio, per teacher, per country, per style, per day-of-week
- **Harmonize teachers** — married names, nicknames, school aliases (e.g., "Sarah Smith" + "Sarah Smith (Jones)" → one entry)
- **Harmonize styles** — collapse "Vinyasa" / "Vinyasa (Power)" / "Vinyasa (Other)" into family buckets per `config/style_buckets.yaml`
- **Classify training hours** — split formal certifications (hours), workshops (single-session), and retreats (immersion practice). See "The three-bucket model" below.

**Run:**
```bash
python scripts/analyze/aggregate_stats.py \
    --input yoga_visits.xlsx \
    --output aggregated_stats.json
```

### Module 3: Output Creation

**Goal:** render the data into shareable artifacts.

**Read first:** `scripts/output/README.md` for theming and chart customization.

**Available outputs:**
- **PowerPoint deck** (`build_deck.js`) — 16-slide narrative arc: title, KPIs, yearly trend, peak moments, geography, top studios, top teachers, style mix, training hours, retreats, what's next, closing reflection
- **HTML dashboard** (`build_dashboard.py`) — single-page dark-theme view with all KPIs and charts inline (base64-embedded PNGs, no external dependencies)
- **Teachers Word doc** (`build_teachers_doc.js`) — sorted table of every teacher with session counts and where they teach now
- **Chart PNGs** (`generate_charts.py`) — standalone matplotlib renders used by all three outputs above

**Run order:**
```bash
python scripts/output/generate_charts.py      # writes PNGs to charts/
python scripts/output/build_dashboard.py      # writes yoga_dashboard.html
node scripts/output/build_deck.js             # writes yoga_journey.pptx
node scripts/output/build_teachers_doc.js     # writes My_Yoga_Teachers.docx
```

## The 19-column schema

This is the canonical row format. Don't deviate without updating the analysis scripts.

| # | Column | Notes |
|---|--------|-------|
| 1 | Date | YYYY-MM-DD or Excel date |
| 2 | Day | Mon/Tue/... (derived but stored) |
| 3 | Time | HH:MM AM/PM |
| 4 | Style (Harmonized) | One of the buckets in `config/style_buckets.yaml` |
| 5 | Class Name (Raw) | Studio-given name |
| 6 | Teacher | Use ` + ` to delimit multiple teachers |
| 7 | Studio | Canonical studio name (see Studios sheet) |
| 8 | City | |
| 9 | State/Province | |
| 10 | Country | "USA" not "United States" |
| 11 | Source | Where this row came from (Gmail/Calendar/Manual/etc.) |
| 12 | Notes | Free text |
| 13 | Unsure Attended | "Y" if you booked but maybe didn't show |
| 14 | Studio Group | Parent brand (e.g., a national chain for all its locations) |
| 15 | Check-in Confirmed | "Y" if cross-referenced with Swarm/Foursquare |
| 16 | Swarm Venue | The Swarm venue name if check-in confirmed |
| 17 | Studio Status | Active / Closed / Renamed |
| 18 | Eventbrite Confirmed | "Y" if matched to Eventbrite |
| 19 | Training | Tag for training-related sessions (see below) |

The xlsx also includes five auxiliary sheets:

- **Studios** — one row per studio with city, status, visit count, last visit, top teacher
- **Instructors** — one row per teacher with primary studio, visit count, first/last visit
- **Planned_Trainings** — upcoming or in-progress trainings (date range, status)
- **Teaching_Log** — for practitioners who also teach (date, location, class taught)
- **Summary** — formula-driven sheet with totals (left for the user to customize)

## The three-bucket model

When totaling "hours," keep three categories separate. Lumping them together produces misleading numbers.

**Training (formal, hour-credentialed):** YTTs (200hr, 300hr, 500hr), specialized certificates (Aerial, Restorative, Anatomy, Inversions, Sadhana, philosophy intensives). These have a credential and a defined hour count. Sum them honestly.

**Workshops (single-session deepening):** breath workshops, mantra workshops, asana clinics, anatomy clinics. Roughly 2–3 hours each. Worth counting but don't conflate with training hours.

**Retreats (multi-day immersion practice):** festival retreats, devotional (bhakti) retreats, studio retreats, adventure retreats, sadhana retreats. Tracked as **sessions, not hours** — typically several practice sessions per day across multiple days. Only count the formal training component (e.g., a daily 1hr philosophy lecture on a sadhana retreat) toward training hours.

**Why this matters:** it is easy to inflate a ~350hr training base to 600hr+ by counting retreat practice as training. The honest split keeps the three columns separate: the formal-training hours, the workshop hours (~a couple dozen), and the retreat sessions (100+) as immersion practice rather than credentialed hours.

## Harmonization patterns

These are the gotchas that cause double-counting if you don't handle them.

**Teacher name variants:**
- Married names: "Sarah Smith" vs "Sarah Smith (Jones)" — pick one canonical form, store the alternate in parentheses
- Nicknames: "Liliana (Lily)" — keep both for searchability
- Abbreviations from booking systems: "Maya O." vs "Maya Okonkwo" — expand to the full name on import where you can confirm identity
- Co-teaching: use ` + ` as a delimiter for two-teacher rows; the analysis scripts split on this

**Studio name variants:**
- Renames: "Riverbend Yoga" → "Stillpoint Yoga" (studio rebrand example) — keep both names if both periods exist in your data, OR collapse and add a Notes column explaining the rename
- Chains: list each location separately with the Studio Group field set to the parent brand
- Retreat venues vs studio-as-retreat-host: "Studio Name (Retreat at Venue)" as a distinct row when the practice happened off-site

**Style variants:** see `config/style_buckets.yaml` — the rule of thumb is that Vinyasa variants collapse to one bucket, Yin and Restorative collapse to one bucket, and "Workshop / Retreat / Hatha" stay separate because they're meaningfully different.

## Privacy & sharing

This skill produces personal data artifacts. The output files contain:
- Names of every teacher the user has practiced with
- Every studio location they've attended
- A timeline of where they've been

When configuring for someone else:
- Set `config/practitioner.yaml` with their name and pronouns if you want personalized output
- The deck and dashboard scripts read this config; they don't hardcode any personal details
- Don't commit `yoga_visits.xlsx` or generated outputs to a public repo — only the templates and scripts

## Customization

**Color palette:** `config/palette.json` controls all chart and slide colors. The default is a warm terracotta / sage / gold palette; replace with your own hex codes.

**Slide order and copy:** `scripts/output/build_deck.js` is intentionally readable rather than abstracted. Edit the slide titles, KPI labels, and section breaks directly.

**Dashboard theme:** `scripts/output/build_dashboard.py` uses CSS variables at the top of the HTML template. Switch to a light theme by inverting the `--bg` and `--text` values.

## Limitations

- **Gmail collection assumes Google Workspace access** via the Gmail API. Adapting for Outlook or other providers requires writing a new collector script.
- **Calendar collection is Google Calendar-only.** Same pattern as Gmail.
- **No automatic dedupe across sources.** The same class might appear in Arketa email, calendar, and manual entry. Review the output of each collection script before merging.
- **No retroactive teacher harmonization.** If you change "Maya O." to "Maya Okonkwo" mid-dataset, you need to re-run the harmonization script across the whole sheet.
- **Cross-system date alignment is manual.** Swarm check-ins use UTC; booking confirmations use local time. Spot-check the day-of-week column to catch timezone drift.

## Quick reference

```bash
# Fresh setup
cp templates/yoga_visits_template.xlsx yoga_visits.xlsx
cp config/example_palette.json config/palette.json
cp config/example_practitioner.yaml config/practitioner.yaml

# Collect (run individually per source)
python scripts/collect/gmail_arketa.py --since 2020-01-01 --out yoga_visits.xlsx
python scripts/collect/calendar_events.py --since 2020-01-01 --out yoga_visits.xlsx

# Analyze
python scripts/analyze/aggregate_stats.py --input yoga_visits.xlsx --output stats.json

# Render
python scripts/output/generate_charts.py --stats stats.json --out charts/
python scripts/output/build_dashboard.py --stats stats.json --charts charts/ --out yoga_dashboard.html
node scripts/output/build_deck.js
node scripts/output/build_teachers_doc.js
```

For deeper detail in any module, read the corresponding `scripts/<module>/README.md`.
