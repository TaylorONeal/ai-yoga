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
| [`yoga-journey`](skills/yoga-journey/) | Compiles your complete training history — every course, certification, and workshop — by gathering the receipts scattered across your email and booking platforms (MINDBODY, Arketa, Momence). |
| [`class-reconstruction`](skills/class-reconstruction/) | Rebuilds a class you taught (or want to re-teach) into a clean, shareable sequence from rough notes, a playlist, or just your memory. |
| [`class-feedback`](skills/class-feedback/) | Turns the scattered impressions after a class into structured, kind, usable notes you can actually learn from. |
| [`yoga-bio`](skills/yoga-bio/) | Writes your teacher bio in three ready-to-use lengths: long (website), short (social), and a studio-submission version. |

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
  yoga-journey/          # Training & certification history compiler
    SKILL.md
  class-reconstruction/  # Rebuild a class from notes or memory
    SKILL.md
  class-feedback/        # Structured post-class reflection
    SKILL.md
  yoga-bio/              # Three-length teacher bio writer
    SKILL.md
```

Each `SKILL.md` is a self-contained, depersonalized template. Fill in the bracketed
`[placeholders]` with your own details, and the skill becomes yours.

## A note on your data

These skills run locally through Claude Code. Some of them (like `yoga-journey`) can read
your email or connected accounts when you ask them to. Nothing is shared back to this
repository — your training records, class notes, and bios stay with you. Treat the
`SKILL.md` files here as blank templates, and keep anything personal out of any copy you
publish or commit.

## Contributing

These are deliberately generic so any teacher can adopt them. If you improve a skill, keep
it depersonalized — no names, studios, or private details in the templates — and open a
pull request.

## License

[MIT](LICENSE) © 2026 Taylor O'Neal
