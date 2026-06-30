---
name: yoga-journey
description: >-
  Compiles a yoga teacher or practitioner's complete training history into a
  single organized record — every teacher training, certification, continuing
  education, and workshop. Use when someone wants to gather, reconstruct, or
  document their yoga journey from scattered sources like email confirmations,
  certificates, and booking platforms (MINDBODY, Arketa, Momence). Triggers on
  requests like "compile my trainings," "build my CE log," "where have I
  studied," or "put together my yoga resume."
---

# Yoga Journey Compilation

Build one clean, chronological record of a person's entire yoga education from
sources that are scattered across inboxes and booking platforms.

## When to use this

- A teacher needs a continuing-education (CE) log for Yoga Alliance renewal.
- Someone is assembling a teaching resume, portfolio, or studio application.
- A practitioner simply wants to remember everywhere they've studied.

## What you'll produce

A single document (the **Journey Record**) containing:

1. **Foundational trainings** — 200hr / 300hr / 500hr and equivalents.
2. **Certifications & specialties** — e.g. prenatal, yin, restorative, trauma-informed,
   meditation, anatomy.
3. **Continuing education & workshops** — shorter trainings, intensives, immersions.
4. **Mentorships & ongoing study** — recurring study with a teacher or lineage.

For each entry, capture as much of this as the sources allow:

| Field | Notes |
| --- | --- |
| Program / course name | The official title |
| Lead teacher(s) | Who taught it |
| School / studio / org | Where it was hosted |
| Hours | CE hours, if applicable |
| Dates | Start–end, or completion date |
| Style / lineage | e.g. Hatha, Vinyasa, Ashtanga, Iyengar, Yin |
| Credential earned | Certificate, RYT level, or "none" |
| Source | Where this entry was confirmed (email, certificate, platform) |

## Where to look (gather sources first)

Ask the user which of these they can connect or share, then search each one:

- **Email** — search the inbox for confirmations and certificates. Useful search terms:
  `teacher training`, `200 hour`, `300 hour`, `certificate`, `enrollment`, `workshop`,
  `continuing education`, `CE`, `immersion`, `registration confirmed`, plus the names of
  any schools or teachers they remember.
- **Booking platforms** — purchase and registration history often lists every workshop
  and training a person has paid for:
  - **MINDBODY** — Account → Purchase History / Visit History.
  - **Arketa** — Profile → Order/Registration history.
  - **Momence** — Account → My Bookings / Purchases.
- **Certificate files** — PDFs or photos in their files, Drive, or photo library.
- **Yoga Alliance profile** — existing logged trainings, if they have one.
- **The user's own memory** — prompt them for trainings the records miss.

> If you have access to the user's email or Drive through a connected tool, offer to search
> it directly. Otherwise, ask the user to export or paste the relevant history and work
> from that.

## Process

1. **Scope it.** Ask what the record is *for* (Yoga Alliance renewal, resume, personal
   archive). That determines how much detail and which fields matter.
2. **Gather.** Pull from every available source above. Note each source so entries can be
   verified later.
3. **Deduplicate.** The same training often appears in both email and a booking platform —
   merge those into one entry, keeping the most complete details.
4. **Fill gaps.** List what's missing (e.g. "hours unknown for [workshop]") and ask the
   user to confirm or supply it. Never invent hours, dates, or credentials.
5. **Organize.** Sort chronologically within each category. Total the CE hours if relevant.
6. **Deliver.** Output the Journey Record as clean Markdown the user can save, plus a short
   summary (e.g. "Found 4 trainings, 6 workshops, 142 CE hours; 3 entries need dates").

## Output format

```markdown
# Yoga Journey — [Name]
_Last compiled: [date]_

## Foundational Trainings
- **[Program name]** — [School], with [Lead teacher]
  [Hours] hrs · [Style] · [Dates] · Credential: [RYT-200 / certificate / none]
  _Source: [email / MINDBODY / certificate PDF]_

## Certifications & Specialties
- ...

## Continuing Education & Workshops
- ...

## Mentorships & Ongoing Study
- ...

---
**Totals:** [X] trainings · [Y] CE hours
**Needs confirmation:** [list any gaps]
```

## Guardrails

- **Accuracy over completeness.** If a detail isn't in a source, mark it `[unconfirmed]`
  and ask — don't guess hours, dates, or credentials.
- **Privacy.** This record is personal. Keep it local; don't post or share it anywhere the
  user didn't ask for.
- **Yoga Alliance note:** CE hour rules and categories change. Remind the user to confirm
  current requirements on yogaalliance.org rather than treating this log as authoritative.

<!--
CUSTOMIZE ME
- Replace the search terms above with your real school/teacher names for faster, more
  accurate email searches.
- If you use a specific booking platform, expand its section with the exact menu path.
- If you keep a master Journey Record file, point this skill at it so updates append
  instead of starting fresh.
-->
