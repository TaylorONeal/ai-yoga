# Continuity and delivery

A daily practice can fail even when the prose is good: the wrong date, an already-used verse, a repeated template, or a second copy of today's entry breaks trust.

## Locate state once

Use an existing user-selected folder or verified storage identifier. Folder titles and modified timestamps cannot distinguish the live collection from a newer backup. Keep backup trees out of rotation searches. On migration, compare entries and exclusions before choosing the new canonical location. Do not copy private state into this skill package.

Recommended private layout, only when starting fresh:

```text
morning-sutra/
  YYYY-MM-DD.md
  _verse-history.json
  _exclusions.md
```

A history record can contain local date, timezone, citation, image, mantra form, closing form, saved path, and delivery status. Existing formats win over this suggestion. Retractions remain in history with their status; exclude them from canonical daily-entry counts, and preserve any explicit instruction never to repeat their verses.

## Retry semantics

| What exists | Next action |
| --- | --- |
| No entry for today's verified local date | Choose a permitted verse and draft |
| Entry saved, history missing | Read the entry and repair history; do not regenerate |
| Entry and history saved, delivery unconfirmed | Inspect the runtime record; report unknown rather than mark delivered by assumption |
| Saved but demonstrably undelivered | Deliver the saved text through the existing authorized path |
| Delivered with no material change | Stay quiet on automatic repeat |
| Explicit correction or rewrite request | Preserve prior version, apply correction, update the canonical reference |
| Multiple same-day copies | Compare content and delivery records; preserve originals and mark the selected canonical copy |

For local writes, use temporary files and atomic rename where available. Update history idempotently by date plus entry identity. If a remote write times out, check whether it succeeded before retrying. If two copies disagree, do not silently merge verse history or overwrite the user's edits.

## Local date

Read a live clock and use an IANA timezone established from current user context. Calculate local midnight to next local midnight in that zone, including daylight-saving transitions. A trip spanning days is not a fresh travel event every day. An optional recurring invitation is not evidence of attendance. If timezone remains unknown, request it before date-sensitive persistence or keep the reflection undated.

## Rotation

Read explicit exclusions and the last 20 canonical entries before choosing. Scan the previous two pieces for image and form as well. A small reference pool is a starting point, never permission to reuse blocked verses. Use a reliable larger edition when the pool runs out. Do not claim that every edition has identical verse counts or numbering.

## Delivery boundary

Do not create schedules, change notification settings, upload the collection, or send messages as a side effect of writing. The runtime's existing authorized route owns delivery. Normal chat output may serve as the delivery; a separate push is usually duplication. Keep logs private and concise.
