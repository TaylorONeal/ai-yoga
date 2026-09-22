# ai-yoga

**Open, AI-powered skills for yoga teachers and practitioners.**

[**Open the visual toolkit →**](https://tayloroneal.github.io/ai-yoga/)

Browse all five skills, copy their full prompts, and get guided installation instructions.
The website is published with GitHub Pages; see [website maintenance](docs/WEBSITE.md).

These are reusable instructions for your AI assistant. Copy a complete prompt from the [visual toolkit](https://tayloroneal.github.io/ai-yoga/) and ask your assistant to save it as a skill, project instructions, or a reusable prompt. If saving is unavailable, use it in the current conversation.
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
| [`class-feedback`](skills/class-feedback/) | Produce feedback on a class in three modes: warm student-facing practice notes, an honest teacher self-review, or a digest of your public student reviews (ClassPass, MINDBODY, and others) read for what actually matters. |
| [`yoga-journey-tracker`](skills/yoga-journey-tracker/) | Build, maintain, and visualize a personal practice log — pull every class, training, and retreat from Gmail, Google Calendar, MINDBODY, and Arketa, then build a reconciled ledger and a retrospective with available output tools. The field guide includes Momence and the wider booking-source workflow; no dedicated Momence API connector is included. |
| [`morning-sutra-mantra`](skills/morning-sutra-mantra/) | A daily poetic contemplation from Patanjali's Yoga Sutras — one sutra, a reflection across life, practice, and relationships, and a mantra to carry. Written from what Claude already knows about you rather than a filled-in profile, and rotates verses so mornings don't repeat. |

### Feeding `class-feedback` (the more, the better)

`class-feedback` gets sharper the more raw material you give it, and nothing is too messy to
help. When you debrief a class, throw in any of these:

- **A post-class voice note.** Record a quick voice memo the moment class ends, while it's
  fresh, then paste the transcript. Rough timestamps make it even better — a line like
  "02:15 the second side felt rushed" lets the feedback line up with a real moment in class.
- **Your class plan in any form.** Typed notes, a screenshot, or a *photo of a handwritten
  sequence on paper* — the skill reads images, and crossed-out lines are useful signal.
- **Your public reviews.** Paste or screenshot what students wrote on ClassPass, MINDBODY,
  Arketa, Momence, Google, or Yelp. The skill reads them for the need underneath the words
  and weighs patterns over one-off bad days, so you get usable signal instead of a sting.

## What's a skill, and how do I use these?

A skill gives your AI a repeatable way to do a particular job. You do not need to start with a terminal or a folder installation.

1. Open the [visual toolkit](https://tayloroneal.github.io/ai-yoga/) and choose a skill.
2. Copy its **prompt**. The full instructions and supporting written guides are included.
3. Paste it into your assistant to use it immediately. Saving it as a reusable skill is optional.
4. Add your material in the indicated space and review the result. The prompt works in a fresh conversation, with no installation needed.

For tasks requiring scripts or file templates, download the complete skill folder from this repository. Your assistant should explain any missing tools, dependencies, or account access rather than claim those were installed by pasting text. Tool-specific folder installation is optional and depends on your assistant.

## Repository layout

```
skills/
  class-reconstruction/  # Rebuild a class from notes, transcripts, or memory
    SKILL.md
  yoga-bio/              # Three-length teacher bio writer
    SKILL.md
  class-feedback/        # Student notes + teacher self-review + reviews digest
    SKILL.md             # (plus scripts/, templates/, references/ — a full multi-file skill)
  yoga-journey-tracker/  # Practice-log compiler + dashboard/deck/teachers-doc generator
    SKILL.md             # (plus scripts/, config/, templates/ — a full multi-file skill)
  morning-sutra-mantra/  # Daily sutra contemplation, personalized from context rather than config
    SKILL.md
    README.md            # Install, scheduling, and privacy notes
```

Each `SKILL.md` is self-contained and depersonalized — no names, studios, or private
details. Where a skill needs your specifics, fill in the bracketed `[placeholders]`.
`morning-sutra-mantra` takes a different approach: instead of placeholders, it draws on whatever
Claude already knows about you from the conversation, memory, and prior sessions.

## A note on your data

The website does not collect your prompts. Your AI provider's policies apply when you paste instructions or personal material into its product. Use available connections only within your authorized scope. Keep personal logs, credentials, workbooks, calendar details, and generated private artifacts outside this public repository. Gitignore rules help but are not a substitute for checking what you publish.

## Contributing

These are deliberately generic so any teacher can adopt them. If you improve a skill, keep
it depersonalized — no names, studios, or private details in the templates — and open a
pull request.

## License

[MIT](LICENSE) © 2026 Taylor O'Neal
