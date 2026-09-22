# Yoga Journey Tracker

The [full skill](SKILL.md) covers collection, evidence-based reconciliation, analysis and presentation of a private practice history. [Booking sources](references/booking-sources.md) include Momence, Mindbody, Arketa, Walla, WellnessLiving, union.fit and the broader historical search playbook.

## Start with a reviewed CSV

Install the full skill folder. Python helpers require `pip install -r requirements.txt` in an isolated environment. Copy the sample schema, populate your own private file, and import into a staged workbook:

```sh
python scripts/collect/manual_csv_import.py /private/path/reviewed-visits.csv --out /private/path/staged-visits.xlsx
python scripts/analyze/aggregate_stats.py --input /private/path/staged-visits.xlsx --output /private/path/stats.json
```

Read the analysis output's population/uncertainty labels. Review a staged copy before updating an existing ledger. Credentials and account access are optional separate setup, not part of a basic manual import.

See [script coverage](scripts/collect/README.md) for implemented collectors and limitations. No dedicated Momence API connector or output-rendering scripts are included. The assistant can work from a Momence export and can create a dashboard/deck/document from reviewed aggregates using available tools.

Keep personal workbooks, tokens, alias maps, source exports and generated artifacts outside the published repository. Empty templates and synthetic examples are for demonstrating structure, not records of a real practitioner.
