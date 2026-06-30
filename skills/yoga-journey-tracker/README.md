# Yoga Journey Tracker

A reproducible system for collecting, analyzing, and visualizing a personal yoga practice log.

Built for the practitioner who has been at it for years, across multiple studios, with class history scattered across Gmail booking confirmations, calendar events, paper notebooks, and memory. This pulls it all into one canonical spreadsheet, then renders that spreadsheet as a dashboard and a presentation.

## What you get

Three connected modules:

1. **Collection** — pull class history from Gmail (Arketa, Mindbody, Walla, WellnessLiving), Google Calendar, Shopify/Stripe receipts, and manual CSV import into a clean 19-column spreadsheet.

2. **Analysis** — aggregate by year, month, studio, teacher, country, style, and day-of-week. Harmonize teacher name variants (married names, nicknames, abbreviations from booking systems). Split training hours into the three buckets that actually make sense: formal certifications, single-session workshops, and multi-day retreat practice.

3. **Output** — render a 16-slide PowerPoint deck, a single-page HTML dashboard with inline charts, and a Word doc listing every teacher you've practiced with.

## Install

```bash
git clone https://github.com/<your-username>/yoga-journey-tracker.git
cd yoga-journey-tracker

# Python deps
pip install -r requirements.txt

# Node deps (for deck and Word doc rendering)
npm install
```

You'll also need:
- Google Cloud credentials for the Gmail and Calendar collectors (see [`scripts/collect/README.md`](scripts/collect/README.md))
- LibreOffice if you want PDF export of the deck (`brew install --cask libreoffice`)

## Quick start

```bash
# Copy templates
cp templates/yoga_visits_template.xlsx yoga_visits.xlsx
cp config/example_palette.json config/palette.json
cp config/example_practitioner.yaml config/practitioner.yaml

# Edit config/practitioner.yaml with your name and pronouns
# Edit config/palette.json if you want different colors

# Collect — one source at a time, review between runs
python scripts/collect/gmail_arketa.py --since 2020-01-01
python scripts/collect/gmail_mindbody.py --since 2018-01-01
python scripts/collect/calendar_events.py --since 2020-01-01

# Analyze
python scripts/analyze/aggregate_stats.py

# Render
python scripts/output/generate_charts.py
python scripts/output/build_dashboard.py
node scripts/output/build_deck.js
node scripts/output/build_teachers_doc.js
```

Outputs land in `output/`:
- `yoga_dashboard.html` — open in any browser
- `yoga_journey.pptx` — PowerPoint, 16 slides
- `My_Yoga_Teachers.docx` — sorted teacher table

## The 19-column schema

Every row is one class attended. The columns:

```
Date | Day | Time | Style (Harmonized) | Class Name (Raw) | Teacher |
Studio | City | State/Province | Country | Source | Notes |
Unsure Attended | Studio Group | Check-in Confirmed | Swarm Venue |
Studio Status | Eventbrite Confirmed | Training
```

Full schema docs in [`scripts/collect/README.md`](scripts/collect/README.md).

## The three-bucket model

Don't lump training, workshops, and retreats into one "hours" total. They mean different things.

| Bucket | What it is | How to count |
|--------|-----------|--------------|
| **Training** | YTTs, formal certifications with hour credit | Sum the hours |
| **Workshops** | Single-session breath / mantra / anatomy / asana clinics | Estimate hours (typically 2–3 each) |
| **Retreats** | Multi-day immersion practice (festival, devotional, sadhana, adventure retreats) | Count sessions and trip count, not hours |

A 200hr YTT is a credential. A 5-day retreat with 8 daily practice sessions is immersion practice, not 40 hours of training. Keep them separate or the numbers lie.

The aggregation script in `scripts/analyze/aggregate_stats.py` enforces this split.

## Why this exists

Most yoga apps track recent classes, not lifetime history. Most spreadsheets are too unstructured for analysis. Most "yoga journey" exports stop at the source studio's records.

This tool sits at the intersection: structured enough to query, flexible enough to handle many years of messy real-world data, and built around the actual sources practitioners use to book classes.

## Privacy

Your data stays local. The Gmail and Calendar collectors run in-process against your Google account; nothing is uploaded anywhere.

The repo intentionally `.gitignore`s `yoga_visits.xlsx` and `output/` so you don't accidentally commit your personal history.

## Contributing

Issues and PRs welcome. Particularly useful:
- New booking system collectors (ClassPass, Glofox, Mariana Tek, etc.)
- Outlook / iCloud Calendar collectors
- Studio name harmonization rules for common chains
- New output formats (PDF report, web app, mobile-friendly dashboard)

## License

MIT. Use it, fork it, ship your own version.

## Acknowledgments

Built from the workflow of a long-time practitioner with a large, messy, multi-country practice history. The schema, the three-bucket model, and the harmonization patterns come from real edge cases hit while compiling that history.
