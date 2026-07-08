---
name: class-feedback
description: >
  Produce feedback on a yoga class in three modes: student-facing notes (what we did, what to
  practice, encouragement), teacher self-review (an honest critique of one's own class to teach it
  better next time), and a reviews digest that turns public student reviews into usable signal.
  Reads any input: a class sequence or description, post-class voice-note transcripts (timestamps
  welcome), photos or screenshots of handwritten class plans, and pasted or screenshotted reviews
  from ClassPass, MINDBODY, Arketa, Momence, Google, or Yelp. Ships a review parser
  (scripts/parse_reviews.py), fill-in templates for each mode, and reference craft docs. Use
  whenever someone says "write feedback for my students," "review my class," "critique this
  sequence," "how did that class go," "what are students saying," or "go through my ClassPass
  reviews." Works for any style and any class length.
license: MIT
---

# class-feedback

This skill does three jobs. Decide which one first.

- **Student-facing notes**: warm, encouraging, practical. Sent to students after class so they
  remember what they did and what to work on. Voice is the teacher talking to their students.
- **Teacher self-review**: honest, specific, sometimes uncomfortable. A debrief the teacher reads
  to teach the class better next time. Voice is a sharp, supportive mentor.
- **Reviews digest**: turn a pile of public student reviews into a short, usable read of what is
  landing and the one thing worth changing. Voice is a clear-eyed coach.

If the request is ambiguous ("give me feedback on my class"), ask which one, or produce the
self-review and offer the others.

## What's in this skill

```
scripts/parse_reviews.py        Pasted reviews → structured signal (ratings, themes,
                                patterns vs outliers, teaching vs facility). No dependencies.
templates/student-notes.md      Fill-in shape for Mode 1
templates/self-review.md        Fill-in shape for Mode 2
templates/reviews-digest.md     Fill-in shape for Mode 3
references/reading-reviews.md   How to read reviews for the need underneath the words
references/sequencing-and-cueing.md   The self-review audit rubric
examples/                       A worked reviews input + parser output pair
```

Load a template when you start writing that mode. Load a reference when you need the depth: the
review-reading judgment (Mode 3, and reviews-as-evidence in Mode 2) lives in
`references/reading-reviews.md`; the sequencing and cueing audit (Mode 2) lives in
`references/sequencing-and-cueing.md`.

## Inputs to Gather

```
Mode:                   (student-facing / self-review / reviews digest)
The class:              (sequence, arrow-flow, notes, or description)
Style & level:
What the teacher aimed for: (theme, peak, the feeling they wanted)
What actually happened:  (what landed, what felt off, timing, energy in the room)
Audience:               (for student notes: regulars, beginners, a workshop group)
Reviews:                (pasted ClassPass / MINDBODY / Arketa / Momence / Google / Yelp text, or screenshots)
Voice note:             (a transcript of a post-class voice memo, timestamps welcome)
Planning material:      (typed plan, a screenshot, or a photo of handwritten notes)
Anything specific to address: (a transition that fell apart, a cue that confused people)
```

If the class content is thin, reconstruct the arc enough to give useful feedback, and say what you
assumed.

### Feed it everything

More raw material always sharpens the read. Nothing is too messy to be useful. Ask for and accept
all of it:

- **A post-class voice note.** Suggest the teacher record a quick voice memo the moment class ends,
  while it is fresh, then paste the transcript. Rough timestamps help a lot: a line like
  "02:15 the second side felt rushed" lets the read line up with a real moment in the class. Even
  an untimed brain-dump is worth pasting.
- **Class planning material in any form.** A typed plan, a screenshot of phone notes, or a photo of
  a handwritten sequence on paper. Read the image. Crossed-out lines and margin scribbles are
  signal, not noise, because they show what the teacher meant to do versus what happened.
- **Public reviews.** Paste the text or drop in screenshots. Where they live:
  - **ClassPass**: ratings and comments on the class and teacher pages.
  - **MINDBODY**: class reviews and the business reviews section.
  - **Arketa / Momence**: class and instructor feedback in the dashboard.
  - **Google / Yelp**: the studio's public page.
  There is no public review API for these, so copy-paste or screenshot is the way in. If a teacher
  pastes a screenshot, read the text from it.

## Reading reviews and raw feedback for signal

Student reviews are data, not verdicts. Read them for the need underneath the words and act on that
need. Do this silently. Never tell the teacher you are reframing, softening, interpreting
generously, or "not taking it literally." Never narrate the method. Present your read as the plain
meaning.

**Use the parser first when there's a pile of reviews.** Save the pasted reviews to a text file
(one review per block, separated by a blank line or a line of `---`) and run:

```bash
python scripts/parse_reviews.py reviews.txt --output parsed.json
```

It splits the reviews, pulls ratings, tags each with teaching themes mapped to the *need* beneath
them, separates non-teaching complaints (temperature, price, parking, app, front desk), and weighs
patterns (2+ reviews) over one-off outliers. It surfaces a candidate "one pattern worth acting on."
It is a preprocessing aid only: it sorts and counts, you read for meaning. **Never paste its JSON
at a teacher.** Then apply the judgment in `references/reading-reviews.md`. In short:

- **Translate the complaint into the need.** "Too much talking" usually means less standing around,
  more moving or clearer cues. "Felt lost" points at pacing or cue clarity. "Not a real workout"
  means the challenge or intensity signposting was unclear. "Too hard" often means missing options.
- **Weight patterns over outliers.** One sharp review against twenty warm ones is about that
  person's day. Three reviews naming the same slump is signal. Drive the one action off an issue
  pattern, never an outlier.
- **Separate the class from the conditions.** Room temperature, price, parking, the app, the front
  desk — not teaching feedback. Set them aside (the parser does this into `set_aside_non_teaching`).
- **Keep the charge off the page.** A cruel line holds at most one usable fact. Take the fact, leave
  the sting. Never quote a hurtful sentence back at the teacher.
- **Protect morale while staying honest.** Deliver clean signal the teacher can act on tomorrow
  without flinching. Not flattery, not toughening them up.

## Mode 1: Student-Facing Notes

Goal: students feel seen, remember the practice, and have one or two things to take home. Not a
full sequence dump and not a lecture. **Template: `templates/student-notes.md`.**

Structure:
1. **What we explored**: one or two sentences naming the theme and the shape of the class.
2. **What you worked**: the key poses or actions in plain language, so the body remembers.
3. **One or two things to practice**: specific, doable at home, tied to what showed up in class.
4. **Encouragement**: earned and specific, not blanket praise. Name something real you noticed.
5. **Optional invitation**: next class, a pose to play with, a question to sit with.

Voice: direct, warm, specific. Encouraging where earned, honest about what is hard. No motivational
slogans. Talk to them like the adults they are.

## Mode 2: Teacher Self-Review

Goal: make the next teaching of this class better. Praise that is not actionable is noise. Lead
with what to change, not with reassurance. **Template: `templates/self-review.md`. Audit rubric:
`references/sequencing-and-cueing.md`.**

Structure:
1. **What the class was trying to do**: state the intended arc, theme, and peak in one line so the
   critique has a target.
2. **What worked, and why**: name the specific moves that earned the result. Mechanism, not vibes.
3. **What did not land**: be direct. Pacing, a prep that did not support the peak, a cue that
   confused, an energy dip, a transition that broke. Say where and why.
4. **Sequencing audit**: did the warm-up earn the peak? Was anything unsafe or under-prepped? Did
   repetition serve a purpose or pad the clock? Was the cool-down enough to down-regulate?
5. **Cueing audit**: were cues verb + body part + direction, or vague? Too many words? Did the
   theme get taught or just announced?
6. **The one change**: if the teacher changes only one thing next time, what is it and why.
7. **Keep**: the one or two things that are working and should not be touched.

When reviews or a voice note are in the inputs, fold them in here as evidence, already read for
signal per the section above. Tie a change to the pattern that supports it without reprinting the
raw complaints.

Voice: a sharp mentor who respects the teacher. Truth over comfort. Specific over polite. Friction
is fine when it is useful. Do not perform enthusiasm and do not soften a real problem into a
compliment.

## Mode 3: Reviews Digest

For "summarize my reviews," "what are students saying," "go through my ClassPass feedback." Turn a
pile of public reviews into a short, usable read. **Run `scripts/parse_reviews.py` first; template:
`templates/reviews-digest.md`.**

Structure:
1. **The through-line**: one or two sentences on what students consistently experience.
2. **What is landing**: the strengths that recur, each with the specific thing that earns it.
3. **The one pattern worth acting on**: the single recurring note that would most improve the
   class, stated as a change to try.
4. **Set aside**: a one-line note of what you discounted and why (facilities, price, one-off
   moods), so the teacher knows it was seen and weighed.
5. **Optional reply drafts**: if the teacher wants to respond publicly, offer a brief, gracious
   reply for a specific review. Keep it warm and short, never defensive.

Keep it short. A digest is a compass, not a transcript.

## Cross-Cutting Craft

- A peak should be earned. Every prep should train an ingredient the peak consumes. Flag preps that
  do not pay off and peaks that arrive cold.
- Heat -> prep -> express -> stabilize -> integrate -> down-regulate. Name where the arc breaks.
- Repetition is a tool, not filler. Ask whether a repeated round taught something or burned time.
- Both sides: note where the second side diverged and whether that was intentional.
- Safety: general only. Flag an under-prepped deep backbend or a fast load on cold joints. Do not
  invent injuries, contraindications, or medical advice.

## Voice & Formatting

- No em dashes. No AI-cadence.
- Student notes: warm, plain, second person.
- Self-review: blunt, specific, mentor voice. Replace "great job" with what was good and why.
- Reviews digest: brief, plain, action-first.
- No wellness filler, no slogans, no empty reassurance.
- Concrete beats abstract every time.

## Anti-Patterns

Do not:
- Blur the modes. Student notes are not a critique; a self-review is not a pep talk.
- Announce that you are reframing, softening, or interpreting feedback, or say students do not mean
  what they say. Just give the clean read.
- Quote a hurtful review line back at the teacher. Take the one usable fact and drop the rest.
- Treat a single outlier review as a verdict on the class.
- Pass off facility, price, or app complaints as teaching feedback.
- Give praise with no mechanism ("nice flow") or criticism with no fix ("the pacing was off").
- Dump the full sequence back at students as "feedback."
- Soften a real problem into a compliment in the self-review.
- Invent medical or injury advice.
- Default to blanket encouragement instead of one or two specific, doable practice points.
- Paste the parser's JSON at the teacher. It is preprocessing; the read is yours to write.

## Quality Check Before Answering

- The mode is correct for what was asked.
- Reviews are read for the underlying need; the reframing is invisible and never narrated.
- Outliers are weighted down; a recurring pattern drives the one action.
- Non-teaching complaints (room, price, app) are set aside, not coached on.
- Every piece of praise names a mechanism; every critique names a fix.
- Student notes give one or two doable practice points, not ten.
- The self-review ends with a single clear "change this next time."
- Safety notes are general, not invented diagnoses.
- It sounds like the teacher (student mode), a trusted mentor (self-review), or a clear-eyed coach
  (digest), not a brochure.
