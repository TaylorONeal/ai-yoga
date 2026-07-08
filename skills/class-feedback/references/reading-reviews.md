# Reading reviews and raw feedback for signal

Read this before writing a reviews digest, or before folding reviews into a
self-review as evidence. It is the judgment layer that sits on top of
`scripts/parse_reviews.py` — the script sorts and counts, this tells you how to
read what it surfaced.

Student reviews are data, not verdicts. Read them for the need underneath the
words and act on that need. Do this silently. Never tell the teacher you are
reframing, softening, interpreting generously, or "not taking it literally."
Never narrate the method. Present your read as the plain meaning.

## Translate the complaint into the need

The surface phrase is rarely the actual problem. Map it down:

| What they wrote | What it usually means | What to act on |
| --- | --- | --- |
| "Too much talking" | Less standing around, more moving or clearer cues | Tighten transitions; cue while moving, not before |
| "Felt lost" | Pacing or cue clarity, not that the class was wrong | Sign-post sides and shape; slow the hand-off between poses |
| "Not a real workout" | The challenge or intensity sign-posting was unclear | Name the effort ("this is the hard part"); offer a harder line |
| "Too hard" | Missing options, not a bad plan | Offer a modification before the shape, not after |
| "Boring" | Predictable arc or an unearned peak | Vary the entry; make the peak feel arrived-at |
| "Too much hands-on" | Consent and calibration, not that assists are bad | Ask first; lighten the pressure; offer opt-out cards |

When you write, present the *need*, not the translation. Write "students want
tighter transitions in the standing series," never "one reviewer said too much
talking but they really mean..."

## Weight patterns over outliers

One sharp review against twenty warm ones is about that person's day, not the
class. Three reviews naming the same ten-minute slump is signal. The parser
encodes this: a theme in 2+ reviews is `is_pattern: true`; a single-occurrence
theme lands in `outliers`. Drive the digest's one action off an **issue
pattern**, never off an outlier — even a vivid one.

## Separate the class from the conditions

Reviews about room temperature, price, parking, the app, or the front desk are
not feedback on teaching. The parser puts these in `set_aside_non_teaching`.
Acknowledge them in one line so the teacher knows they were seen and weighed,
then set them down. Do not coach the teacher on the studio's thermostat.

## Keep the charge off the page

A cruel line still holds at most one usable fact. Take the fact, leave the sting.
Never quote a hurtful sentence back at the teacher. "This teacher is a
condescending mess who wasted my hour" becomes, if anything, one line about tone
landing as condescension for at least one student — and only if a pattern backs
it. If nothing backs it, it is one bad day; drop it.

## Protect morale while staying honest

Deliver signal the teacher can act on tomorrow without flinching. This is not
flattery and it is not toughening them up. It is clean signal: the strengths
that recur (so they keep doing them), and the single most useful change (stated
as a thing to try, not a failing).

## Resolving "mixed" themes

The parser tags `music` and `adjustments` as mixed — they can show up as praise
in one review ("perfect playlist") and a complaint in another ("too loud"). The
count can't tell direction. Read the individual reviews (each carries its
`teaching_themes` and `sentiment`) to decide which way a mixed theme actually
leans before you put it in the digest.
