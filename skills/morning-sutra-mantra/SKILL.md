---
name: morning-sutra-mantra
description: >
  Daily poetic yoga-sutra contemplation, written for whoever is running it. Writes a single
  Patanjali sutra as the day's seed, a short grounded reflection across daily life, practice, and
  relationships, a carryable mantra, and a closing invitation toward presence and equanimity. Draws
  on whatever the assistant already knows about the reader (conversation history, memory files,
  prior sessions, connected calendar) instead of a filled-in profile, and rotates sutras so the same
  verse does not repeat across nearby mornings. Use when a scheduled morning run fires, or when the
  reader asks for their morning contemplation, today's sutra, a morning mantra, or a soul-facing
  counterpart to a logistics briefing. This is poetry and presence, never a schedule readout.
---

# Morning Sutra Mantra

Write a daily morning contemplation for the person running this skill. This is a poetic,
soul-facing practice, not a logistics briefing. It should help the reader feel present, alive, free
to savor the day, and settled in equanimity.

There is nothing to configure. The skill writes for whoever is on the other end of the
conversation, using what is already known about them rather than a filled-in template.

## Know the reader before you write

Before writing, gather whatever context is actually available. Use what exists; never invent what
does not.

- **This conversation and prior sessions.** Name, how they relate to yoga (new practitioner,
  longtime teacher, coming back after time off), things they have mentioned about their week,
  their people, what they are carrying right now.
- **Memory or profile files**, if this environment keeps one (a `CLAUDE.md`, a user memory store,
  notes from earlier runs of this or other skills in this repo, e.g. a bio from `yoga-bio` or a
  practice log from `yoga-journey-tracker`). Read them if they are there; do not ask the reader to
  fill out a form first.
- **A connected calendar**, if one is available in this session. Skim today's events for real
  texture: a class they teach, a hard meeting, travel, a person they are about to see. Let it
  quietly inform the reflection. If nothing is connected, or the calendar is empty, proceed without
  it.
- **If this is the first run and nothing is known yet**, do not interrogate the reader with an
  intake form. Write a shorter, quieter contemplation that leans on the sutra itself rather than
  invented specifics, and let it get more textured on the next day once you know more of them.

Never state your sources out loud ("I checked your calendar," "based on your memory file"). The
knowing should be invisible. It should just read like someone who knows them wrote it.

## Rotate the sutra

Keep a small local log next to this skill, `.sutra-log.md` (create it on first run if it does not
exist), with one line per morning: the date and the sutra citation used, oldest first.

Before choosing today's sutra:
1. Read the log.
2. Rule out any sutra cited in the last 14 entries (or all of them, if fewer than 14 exist).
3. Choose freely from the remaining verses across all four chapters (Samadhi, Sadhana, Vibhuti,
   Kaivalya) — not just the handful everyone quotes. There are 196 sutras; use the range.
4. After writing, append today's date and the citation to the log.

If the log does not exist yet, start it fresh and do not treat the absence of history as a reason
to default to the most familiar verse (1.2, 2.46, 2.1) — pick with the same range you would if the
log were full.

This log is personal state, not repo content. Do not commit it; add it to `.gitignore` in whatever
project or home directory it lives in.

## What to produce each morning

1. **One sutra as the day's seed.** Cite it (e.g. "Yoga Sutra 1.2, yogash chitta vritti
   nirodhah"). Give the Sanskrit, then a plain, felt translation in your own words, not a
   textbook gloss.

2. **A short reflection, 4 to 8 sentences.** Apply the sutra to three living arenas: the reader's
   daily life, their yoga practice, and their relationships. Be specific and concrete, using what
   you actually know about this person and, if available, today's shape. Name real textures of a
   day, real moments on the mat, real friction and tenderness between people. This is where the
   depth lives. If you know little about the reader yet, write it a touch more universal rather
   than inventing detail.

3. **A mantra for the day.** One line, maybe two. Something the reader can carry, repeat, and
   return to. First person or direct address. It should land in the body, not just the mind.

4. **A closing invitation, one or two sentences.** Point toward savoring, presence, and
   equanimity. Name an actual small thing to feel or notice today, not a self-help directive.

## Voice

- No em dashes. Use commas, periods, or line breaks.
- No AI cadence. No rule-of-three constructions, no "not just X but Y" parallelism, no
  motivational-poster energy, no TED-talk voice.
- Poetic but grounded. Specific over polished. Concrete images over abstractions. Write like a real
  poet who practices, not a wellness app.
- Draw on the contemplative and non-dual traditions the practice lives in (yoga, Advaita, Buddhist
  loving-kindness) without name-dropping them as decoration. Let the wisdom be felt, not cited
  beyond the one sutra.
- Fewer words is usually better. Do not pad.

## Format

Deliver as a clean, readable message with light structure: the sutra, the reflection, the mantra
set off on its own line, then the closing. No heavy markdown, no emoji, no headers-as-labels beyond
what makes it breathe. This is meant to be read slowly with coffee.

## Self-check before delivering

- Strip any em dashes, any AI-cadence tells, any generic advice. If it reads like a chatbot,
  rewrite it until it reads like a person who means it.
- Confirm today's sutra is not in the last 14 log entries, and that the log has been updated.
- Confirm nothing about the reader was invented — everything specific came from real context.

See this skill's [README](README.md) for install, scheduling, and privacy notes on the rotation
log.
