# Morning Sutra Mantra

A daily poetic contemplation built from Patanjali's Yoga Sutras, written for whoever runs it.

Each morning it picks one sutra, writes a short reflection that touches daily life, practice, and
relationships, gives you a one-line mantra to carry, and closes with an invitation toward presence
and equanimity. It is a soul-facing companion piece to a logistics briefing, not a schedule
readout.

## What makes it "personalized"

There is no profile to fill out. Instead of a `CONFIG` block asking for your name and practice
background, this skill instructs Claude to draw on what it already knows about you: this
conversation, memory files it has access to, prior sessions, and output from other skills in this
repo (a bio from `yoga-bio`, a practice log from `yoga-journey-tracker`) if those are present. If a
calendar is connected, it reads today's shape quietly for texture, never as a schedule dump.

The first run, before Claude knows much about you, is intentionally shorter and leans on the sutra
itself rather than invented detail. It gets more textured over time as it learns more about you,
the same way a person would.

## Rotation

The skill keeps a small local log, `.sutra-log.md`, of the date and sutra cited each morning it
runs, and rules out anything from the last 14 entries before picking the next one. That log is
personal state, not repo content — see [Privacy](#privacy) below.

## Install

```bash
git clone https://github.com/tayloroneal/ai-yoga.git
cp -r ai-yoga/skills/morning-sutra-mantra ~/.claude/skills/
```

Or copy it into a project's `.claude/skills/` folder.

## Use

Ask for it directly, e.g. "give me my morning contemplation" or "what's today's sutra," or invoke
it by name with `/morning-sutra-mantra`. To have it run on its own each day, register it with a
morning trigger in your agent runtime (for example, a 6:30am daily schedule) and have that trigger
deliver the result wherever you'll see it.

## Privacy

`.sutra-log.md` is created next to this skill the first time it runs and lives on your own
machine. It never leaves your environment and is not part of this repository — this folder's
`.gitignore` keeps it out of any commit. If you install this skill somewhere without that
`.gitignore` in effect (a monorepo, a different skills folder), add `.sutra-log.md` to that
project's `.gitignore` yourself.

## License

[MIT](../../LICENSE). Sutra numbering and Sanskrit are from Patanjali's Yoga Sutras, public domain.
