# Analysis module

Takes a populated `yoga_visits.xlsx` and produces `aggregated_stats.json` plus harmonization passes that clean up the data in place.

## Run order

```bash
# 1. Harmonize (idempotent — safe to re-run)
python scripts/analyze/harmonize.py --input yoga_visits.xlsx

# 2. Classify training tags (idempotent)
python scripts/analyze/classify_training.py --input yoga_visits.xlsx

# 3. Aggregate stats
python scripts/analyze/aggregate_stats.py --input yoga_visits.xlsx --output stats.json
```

## What each script does

### `harmonize.py`

Walks the Yoga Visits sheet and normalizes:

- **Teacher name variants** — looks for known aliases (loaded from `config/teacher_aliases.yaml`) and rewrites them in place. E.g., "Maya O." → "Maya Okonkwo", "Priya Sharma" → "Priya Anand (Sharma)".
- **Style strings** — collapses raw style values into the buckets defined in `config/style_buckets.yaml`. So "Power Vinyasa (Heated)" and "Heated Power" both become "Vinyasa (Power/Heated)".
- **Studio names** — handles renames (e.g., a studio that changed its name) by mapping the old name to the new canonical name and adding a Notes column entry.
- **Country codes** — normalizes "United States" → "USA", "Mexico" → "Mexico", etc. so country-level rollups work.

Aliases are read from `config/teacher_aliases.yaml` and `config/studio_aliases.yaml`. Edit those to add your own mappings.

### `classify_training.py`

Looks at each row and sets the Training column (col 19) based on:
- Class name (e.g., "200hr Teacher Training Module 3" → "200hr YTT")
- Studio (e.g., a retreat venue → "Multi-day retreat")
- Notes (manual override)
- Style bucket (e.g., "Retreat / Workshop" → "Workshop" if 1 day, "Multi-day retreat" if 3+ days)

The tag set is defined in `config/training_tags.yaml`.

Re-running is safe: existing tags are preserved unless `--overwrite` is passed.

### `aggregate_stats.py`

Produces a single JSON file with everything the output renderers need:

```json
{
  "total_visits": 1200,
  "first_year": 2013,
  "last_year": 2026,
  "years_active": 14,
  "unique_studios": 150,
  "unique_teachers": 185,
  "unique_countries": 12,
  "unique_cities": 48,
  "avg_per_year": 92.3,
  "yearly": [...],
  "monthly": [...],
  "top_studios": [...],
  "top_teachers": [...],
  "top_countries": [...],
  "styles": [...],
  "dow": [...],
  "training_tags": [...],
  "training_hours": {
    "formal": 360,
    "in_progress": 300,
    "workshops": 30
  },
  "retreats": {
    "session_count": 110,
    "trip_count": 15
  },
  "peak_year": [2025, 215],
  "dna": {
    "intl_visits": 130,
    "lifetime_avg_per_week": 1.8
  }
}
```

## Customization

### Teacher aliases (`config/teacher_aliases.yaml`)

```yaml
aliases:
  "Maya Okonkwo":
    - "Maya O."
    - "Maya O"
    - "Maya Okonkwo (formerly Maya Vance)"
  "Priya Anand (Sharma)":
    - "Priya Sharma"
    - "Priya Anand"
    - "Priya A"
```

### Studio aliases (`config/studio_aliases.yaml`)

```yaml
aliases:
  "Stillpoint Yoga":
    - "Riverbend Yoga"
    - "Riverbend Yoga / Stillpoint Yoga"
    - "Riverbend"
renames:
  "Riverbend Yoga":
    new_name: "Stillpoint Yoga"
    rename_year: 2026
    note: "Riverbend renamed to Stillpoint in 2026"
```

## The three-bucket model

`aggregate_stats.py` enforces the split. The output `training_hours.formal` sums only rows tagged with formal training tags (`200hr YTT`, `50hr (Aerial)`, etc. — see `config/training_tags.yaml`). Workshops are a separate count. Retreats are reported as `session_count` and `trip_count`, never hours.

If your `featured_trainings` in `config/practitioner.yaml` includes a manual hour count (e.g., for trainings that don't have one tag per session in your data), the aggregator uses your manual count rather than counting tagged sessions.

## Sanity checks the aggregator runs

After aggregation, the script prints warnings for:

- Studios with 0 visits but listed in the Studios sheet
- Teachers with no sessions but listed in the Instructors sheet
- Years with anomalous gaps (e.g., 0 visits flanked by 100+ visit years)
- Rows missing a Country (rolls up as blank in the countries chart)
- Rows where Day-of-week doesn't match the Date column (timezone artifact)

These don't block the run; they're FYI.
