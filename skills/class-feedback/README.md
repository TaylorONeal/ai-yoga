# class-feedback

**Turn a class you just taught into feedback you can use.**

A [Claude Code](https://claude.com/claude-code) skill that does three related
jobs for a yoga teacher, and knows which one you're asking for:

1. **Student-facing notes** — warm, practical notes to send students after class
   so they remember what they did and what to practice.
2. **Teacher self-review** — an honest, specific debrief you read to teach the
   class better next time. A sharp, supportive mentor, not a pep talk.
3. **Reviews digest** — turn a pile of public reviews (ClassPass, MINDBODY,
   Arketa, Momence, Google, Yelp) into a short, usable read of what's landing and
   the one thing worth changing.

It reads anything you give it: a sequence or description, a post-class voice-note
transcript, a photo of a handwritten class plan, or pasted/screenshotted reviews.

## What's in here

```
class-feedback/
  SKILL.md                     # the operational skill Claude runs
  README.md                    # this file
  scripts/
    parse_reviews.py           # pasted reviews → structured signal (no deps)
    README.md
  templates/
    student-notes.md           # the three output shapes, ready to fill
    self-review.md
    reviews-digest.md
  references/
    reading-reviews.md         # how to read reviews for the need underneath
    sequencing-and-cueing.md   # the self-review craft rubric
  examples/
    example_reviews.txt        # a worked input...
    example_parsed.json        # ...and its parser output
```

This is both a **README** (this file, project-facing) and an **actual skill**
(`SKILL.md` plus runnable scripts, templates, and reference docs) — not just
prose instructions.

## Install

```bash
git clone https://github.com/tayloroneal/ai-yoga.git
cp -r ai-yoga/skills/class-feedback ~/.claude/skills/
```

Or drop it in a project's `.claude/skills/` folder to share with collaborators.
The review parser is pure Python standard library — nothing to `pip install`.

## Use

Open Claude Code and describe what you want:

> "Write feedback notes for my students from tonight's class."

> "Give me an honest self-review of this sequence — here's my voice memo."

> "Go through my ClassPass reviews and tell me what to work on."

Claude picks the mode from what you ask. If it's ambiguous ("give me feedback on
my class"), it will ask which one, or produce the self-review and offer the rest.

### The reviews digest, hands-on

You can also run the review parser directly to see the structured signal before
the write-up:

```bash
# Paste your reviews into a text file, one per block (blank line or --- between)
python scripts/parse_reviews.py my_reviews.txt --output parsed.json

# Or pipe from the clipboard (macOS)
pbpaste | python scripts/parse_reviews.py -
```

It splits the blob into individual reviews, pulls out ratings, separates teaching
feedback from facility/price/app complaints, buckets recurring themes, and weighs
patterns (2+ reviews) over one-off outliers. See
[`examples/`](examples/) for a worked pair and
[`scripts/README.md`](scripts/README.md) for details.

## Feed it everything

The skill gets sharper the more raw material you give it, and nothing is too
messy to help:

- **A post-class voice note.** Record a memo the moment class ends, while it's
  fresh, then paste the transcript. Rough timestamps ("02:15 the second side felt
  rushed") let the read line up with a real moment.
- **Your class plan in any form.** Typed notes, a phone screenshot, or a *photo
  of a handwritten sequence* — the skill reads images, and crossed-out lines are
  signal.
- **Your public reviews.** Paste the text or drop in screenshots. There's no
  public review API for these platforms, so copy-paste or screenshot is the way
  in.

## A note on your data

Everything runs locally through Claude Code. Reviews and class material you feed
it stay on your machine — nothing is shared back to this repo. The bundled
`.gitignore` keeps your real `reviews.txt` and generated `parsed.json` from being
committed, while still shipping the depersonalized example pair. Keep anything
personal out of any copy you publish.

## License

[MIT](LICENSE). Use it, fork it, ship your own version.
