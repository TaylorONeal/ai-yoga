# Scripts

One helper lives here. It is an **aid to the reviews-digest mode**, not the
whole skill — the student-notes and self-review modes are writing tasks driven
by the templates and reference docs, not by code.

## `parse_reviews.py`

Turns a blob of pasted reviews into structured signal so the human read can
focus on judgment instead of counting. Pure standard library, no dependencies,
Python 3.8+.

```bash
# From a file of pasted reviews
python scripts/parse_reviews.py reviews.txt

# Write the JSON out and print a summary
python scripts/parse_reviews.py reviews.txt --output parsed.json

# Pipe from the clipboard (macOS)
pbpaste | python scripts/parse_reviews.py -
```

**Input format.** One review per block. Separate blocks with a blank line or a
line of `---`. A rating anywhere in a block is picked up (`5 stars`, `5/5`,
`Rating: 4`, `★★★★☆`, or a leading `5 -`); blocks without a rating are still
parsed.

**What it does.**
- Splits the blob into individual reviews and pulls a rating from each.
- Tags each review with **teaching themes** (pacing, cue clarity, intensity,
  options, sequencing, cueing, theme, atmosphere, adjustments, music, voice) and
  maps each theme to the *need underneath the words*.
- Separates **non-teaching complaints** (temperature, price, parking, the app,
  the front desk, facilities) into a set-aside bucket.
- **Weighs patterns over outliers**: a theme in 2+ reviews is a pattern; a theme
  in exactly one review is an outlier to note, not act on.
- Proposes **one issue pattern worth acting on** (the most frequent teaching
  issue).

**What it does NOT do.** It doesn't write the digest, decide what the teacher
should change, or judge tone. It sorts and weighs; a person reads the result.
Themes tagged "mixed" (music, adjustments) can land in both the praise and issue
lists because the keyword match can't tell direction per mention — resolve those
by reading the reviews. **Never paste this JSON at a teacher as feedback.**

See [`../references/reading-reviews.md`](../references/reading-reviews.md) for
how to turn the buckets into a usable read, and
[`../examples/`](../examples/) for a worked input/output pair.

### Extending the theme taxonomy

The theme lists (`TEACHING_THEMES`, `NON_TEACHING_THEMES`) are plain data at the
top of the script. Add a dict with `key`, `label`, `need`, `polarity`
(`issue` / `praise` / `mixed`), and a list of regex `patterns` to teach it a new
recurring complaint or strength. Keep patterns lowercase-insensitive and
conservative — a false theme hit is worse than a miss, because the whole point is
trustworthy signal.
