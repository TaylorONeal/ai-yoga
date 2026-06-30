# ai-yoga

**Open, AI-powered skills for yoga teachers and practitioners.**

These are small, focused tools you run with [Claude Code](https://claude.com/claude-code).
Each one does a piece of the invisible work that surrounds teaching yoga — gathering your
training history, rebuilding a class from memory, capturing feedback, writing your bio — so
you can spend less time at a keyboard and more time on the mat.

---

## Why this exists

Yoga teachers carry an enormous amount of knowledge that lives in messy, scattered places:

- **Trainings** buried across years of email confirmations, certificates, and three
  different booking platforms.
- **Classes** that took weeks to design and then vanish the moment everyone rolls up
  their mats.
- **Feedback** — what landed, what didn't, who you adjusted — that never gets written
  down and is gone by the next morning.
- **Bios** that have to be rewritten, slightly differently, for every studio website,
  workshop flyer, and social profile.

None of this is teaching. All of it takes time. These skills do that administrative and
reflective work for you, in your voice, on your own machine.

## Who this is for

- Independent and traveling yoga teachers
- Teachers-in-training and recent grads (200hr / 300hr / 500hr) building a portfolio
- Substitute teachers reconstructing a class on short notice
- Studio teachers who want their own records, separate from any studio's system
- Dedicated practitioners tracking their own journey

> **Running a studio?** These skills are for the *individual teacher or practitioner*, not
> the studio back office. If you need scheduling, booking, payments, or membership
> software for a studio, look at the **Tandava Studio** project instead — that's the
> studio-facing counterpart to this teacher-facing toolkit.

---

## The tools

| Skill | What it does |
| --- | --- |
| [`class-reconstruction`](skills/class-reconstruction/) | Reconstruct a yoga class sequence from messy notes, transcripts, photos, or memory — from a one-line flow map to a full teaching dossier with honest, per-section confidence labeling. |
| [`yoga-bio`](skills/yoga-bio/) | Generate a yoga teacher bio in three lengths — a short schedule blurb, a medium website "about," and a full bio page — in your voice, not wellness-brochure filler. |
| [`class-feedback`](skills/class-feedback/) | Produce feedback on a class in two modes: warm student-facing practice notes, or an honest teacher self-review to teach it better next time. |
| [`yoga-journey-tracker`](skills/yoga-journey-tracker/) | Build, maintain, and visualize a personal practice log — pull every class, training, and retreat from Gmail, Google Calendar, MINDBODY, and Arketa, then render a dashboard, a slide deck, and a teachers document. |

## What's a "skill," and how do I use these?

A **skill** is a folder with a `SKILL.md` file inside it. It's plain text — instructions
that tell Claude Code how to do one specific job well. You don't have to write code to use
them.

### Install

Copy the skills you want into your Claude Code skills directory:

```bash
# Clone this repo
git clone https://github.com/tayloroneal/ai-yoga.git

# Copy a skill (or all of them) into your personal skills folder
cp -r ai-yoga/skills/yoga-bio ~/.claude/skills/
```

Or copy them into a project's `.claude/skills/` folder to share with collaborators.

### Use

Open Claude Code and just describe what you want, e.g.:

> "Write my teacher bio in long, short, and studio versions."

> "Help me reconstruct the vinyasa class I taught last Tuesday."

Claude picks the right skill automatically based on what you ask. You can also invoke one
directly by name (e.g. `/yoga-bio`).

---

## Repository layout

```
skills/
  class-reconstruction/  # Rebuild a class from notes, transcripts, or memory
    SKILL.md
  yoga-bio/              # Three-length teacher bio writer
    SKILL.md
  class-feedback/        # Student notes + teacher self-review
    SKILL.md
  yoga-journey-tracker/  # Practice-log compiler + dashboard/deck/teachers-doc generator
    SKILL.md             # (plus scripts/, config/, templates/ — a full multi-file skill)
```

Each `SKILL.md` is self-contained and depersonalized — no names, studios, or private
details. Where a skill needs your specifics, fill in the bracketed `[placeholders]`.

## A note on your data

These skills run locally through Claude Code. Some of them (like `yoga-journey-tracker`) can
read your email or connected accounts when you ask them to, and write data files on your own
machine. Nothing is shared back to this repository — your training records, class notes, and
bios stay with you. The `yoga-journey-tracker` skill ships a `.gitignore` that keeps your
personal `yoga_visits.xlsx`, credentials, and generated outputs from ever being committed.
Treat the `SKILL.md` files here as blank templates, and keep anything personal out of any copy you
publish or commit.

## Contributing

These are deliberately generic so any teacher can adopt them. If you improve a skill, keep
it depersonalized — no names, studios, or private details in the templates — and open a
pull request.

## License

[MIT](LICENSE) © 2026 Taylor O'Neal
