# Analysis helpers

`aggregate_stats.py` reads the `Yoga Visits` sheet by header and reports confirmed-only totals by default. `--include-provisional` explicitly widens the population; the JSON labels that choice. Empty workbooks are valid. Undated records are counted for review and excluded from dated metrics.

```sh
python scripts/analyze/aggregate_stats.py --input /private/path/visits.xlsx --output /private/path/stats.json
```

A positive `Check-in Confirmed` or explicit `Attendance Status` is required for confirmed totals. `Unsure Attended` remains provisional; cancellation/no-show statuses override confirmation. Existing 19-column ledgers may add `Attendance Status`, or maintain status in a reconciled export. A blank uncertainty cell alone is not confirmation.

The output counts visits and distinct practice days separately. Co-teachers separated with ` + ` count as individuals. Alias/location reconciliation happens before aggregation. It does not automatically prove two rows refer to distinct classes.

For training hours pass `--config /private/path/practitioner.yaml`. Only `featured_trainings` with `status: completed` and explicit finite nonnegative hours count toward known formal hours; in-progress and workshops are separate. Missing hours stay visibly unknown. No row tag or default workshop duration invents a credential.

This replaces the earlier inferred-hours JSON contract. Renderers must read `population`, `attendance_counts`, and `training_hours.*.known_hours/entries_without_hours` and must not treat missing evidence as zero. No output renderers ship here.

`harmonize.py` applies reviewed alias files. `classify_training.py` proposes tags from keywords; tags classify records and do not establish completion or earned hours. Run either on a staged workbook and review changes before replacing a canonical copy.
