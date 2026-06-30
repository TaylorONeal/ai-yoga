---
name: class-reconstruction
description: >
  Reconstruct a yoga class sequence from messy, incomplete, or multi-source input: handwritten
  notes, OCR, auto-transcribed audio, PDF transcripts with errors, post-class memory, or photos of
  binder pages. Default output is a concise arrow-flow map; on request, produces a full teaching
  dossier with honest per-section confidence labeling, a teacher fingerprint, a peak scaffold, and
  rich metadata. Use whenever someone provides raw class notes or transcript material and wants a
  usable reconstruction, even if they just say "help me figure out what we did," "reconstruct this
  sequence," "clean up these notes," "what was that flow," or "make a dossier." Applies to any yoga
  style (Ashtanga, Vinyasa, Yin, etc.) and any source quality.
---

# class-reconstruction

Reconstruct yoga class sequences from noisy, incomplete, or multi-source input. Produce honest,
usable teaching documents in a consistent format, from a one-line flow map up to a full dossier.

## Core Principle

Separate what is **strongly supported**, what is **likely but inferential**, and what is **too
weak to claim**. The goal is not perfect historical recovery. The goal is a useful, honest,
teachable reconstruction. Never write a reconstruction as if it were exact when it is not.

## Behind-the-Scenes Rule

The reconstruction is the artifact. How it was made is not.

Do not reference transcripts, recordings, audio, voice memos, OCR, auto-transcription, or "the
source file" anywhere in the finished document. The document reads as if reconstructed from class
observation and post-class memory.

- Confidence labels say "strongly supported / likely / best guess." They do not say
  "transcript-confirmed" or "memory-based."
- The closing meta section is called **Reconstruction Notes** and may say it is a single-pass
  reconstruction "based on class observation and post-class memory, cross-referenced with the
  teacher's prior classes." Nothing about how the raw material was captured.

## Pick the Output Mode First

Choose the lightest mode that satisfies the request. Do not default to the full dossier.

1. **Concise reconstruction (DEFAULT).** For "reconstruct this," "what was that class," "clean up
   these notes." A clean arrow-flow map, optionally with short sequence-logic notes and a sparse
   cue thread. Chat output, no file.
2. **Expanded teaching notes.** For "give me teaching notes," "a class plan I can study." The
   concise flow plus scaffold, fuller cue thread, timing.
3. **Full dossier.** For "make a dossier" or a polished teaching-study artifact. See Full Dossier.
4. **Cue-only.** For "just the intro," "the peak cues." Teacher-voice cueing, no full sequence.

When unsure between concise and dossier, produce concise and offer to expand.

## The 7-Step Method

### Step 1: Gather Inputs
Collect everything available before reconstructing: raw notes, any source material, memory
corrections ("no warrior three," "6 Sun As, 4 guided, 2 on our own"), teacher and style context
(name, style, lineage, pacing, cueing voice), and document preferences. If key context is missing
(teacher, date, style), ask once before proceeding. If a public bio or lineage is available, pull
it: it anchors voice and method.

### Step 2: Extract Signal
Pull every likely pose, transition, rhythm cue, and repeated phrase. Do not force order yet. On
noisy input, expect chronic word-level errors and triage hard: the first chunk is often
unrecoverable noise; real cueing usually starts at the first prop call or clear instruction. Keep
the legible signal, label the rest honestly.

### Step 3: Group by Class Phase
Sort fragments into buckets: arrival/meditation, warm-up/spinal prep, sun salutations, standing
flow, balance/peak setup, peak, backbends, floor work, cool down/savasana, closing philosophy.

### Step 4: Resolve Contradictions
Priority when sources disagree: (1) explicit corrections, (2) teacher debrief or recap, (3)
repeated notes over one-off fragments, (4) corroborated pose names over garbled singles.

### Step 5: Rebuild the Arc
Assemble the most coherent sequence that matches the teacher's style, preserves the strongest
signals, follows sane sequencing logic (heat -> prep -> express -> stabilize -> integrate ->
down-regulate), and does not invent complexity. Use the Heuristics below to bridge gaps.

### Step 6: Stress Test
Ask: what breaks if this pose is removed? Does this prep support the later peak? Is a repeated
flow actually repeated or just duplicate notes? Am I claiming more than the evidence supports?

### Step 7: Label Confidence
Use these terms consistently, **per section, never as one blanket score**:
- **Strongly supported**: multiple signals agree, or confirmed
- **Likely**: one clear signal, consistent with style
- **Best guess**: reasonable inference, no direct confirmation
- **Unclear**: flagged fragment, could not resolve
- **Optional / layered**: teacher may have offered; not confirmed

When a pose is corrected ("that wasn't Pigeon, it was a lunge reach"), propagate the fix through
every section in one pass. Do not leave stale references.

## Reconstruction Heuristics

When the source is incomplete, choose the most likely bridge:

- Table / child's pose usually leads to Down Dog.
- Down Dog often leads to Three-Legged Dog, knee-to-nose, lunge, twist, or half split.
- Surya A/B/C usually appears before the largest standing arc.
- Crescent / High Lunge often opens the standing sequence.
- Warrior II -> Reverse -> Triangle is a common stable spine.
- Triangle often prepares Half Moon, Sugarcane, or Standing Split.
- Wide Fold / Skandasana often appears after Triangle/Half Moon arcs.
- Plank / Side Plank / Chaturanga often resets or strengthens after standing work.
- Bridge / Wheel usually precedes supine twist, happy baby, or rest.

Use these to infer, not to invent. A bridged pose is "likely" or "best guess," never "strongly
supported."

## Concise Reconstruction Format (default)

```text
Opening -> Warm-Up -> Down Dog -> Sun Salutations -> Right Side: ... -> Reset/Vinyasa ->
Left Side Repeat -> Backbend -> Cooldown -> Rest
```

Then add, only if helpful:

```markdown
**Sequence logic:** 2 to 4 short lines about the arc, peak, or repeated pattern.
**Cue thread:** 3 to 6 short lines in the teacher's voice.
**Notes:** assumptions, missing pieces, or safety flags.
```

Style: arrow notation for the main flow, phase labels over per-transition narration, right/left
markers where the standing sequence branches, breath as the organizing principle. Preserve counts
and repeats (`x2-3`, `x6`, `repeat x3`, `self-paced`, `option`). Rebuild the second side only when
clearly symmetrical, and label it "Left Side Repeat" rather than rewriting every pose.

## Full Dossier

### Document Sections, in order

1. **Title**: the class *dharma* as the title (e.g. "Stay Rooted, Stay Open"), not a generic
   descriptor. Teacher + studio + city as a byline. Date + time + class type beneath.
2. **Subtitle**: one italic line naming the through-line.
3. **Class Details**: the structured facts box (fields below, including Teacher Signature).
4. **Context / Theme Note**: a callout: the room, the dharma, why the class was shaped this way.
5. **Flow at a Glance**: abbreviated arrow-chain by phase (Ground / Rise / Heat / Stand / Arc /
   Peak / Close), with an abbreviation key. The script-scannable top reference.
6. **Class Snapshot**: one prose paragraph.
7. **Class Arc**: a horizontal strip with time markers and a peak/standard/cool legend.
8. **Simplified Flow**: arrow-chain lines per phase, one bold phase label each, cue language woven
   in. Mirror noted as "*Mirror on left.*" not a duplicated block.
9. **Right <-> Left Mirror table**: see Mirror Table Format.
10. **How the Peak Is Earned**: layered scaffold table; each layer trains an ingredient the peak
    consumes.
11. **Notes**: the structural observations.
12. **Dharma in Physics**: the class's central teaching as opposing-force pairs across the shapes
    that use it. Prose lead, then a `Shape | force in | <-> | force out` table.
13. **Cue Thread by Phase**: teaching cues per phase, in the teacher's voice.
14. **Teaching Script**: continuous, teachable start-to-finish script in the teacher's voice.
    Verb + body part + direction is the core cue structure.
15. **Why It Works**: prose, the sequencing logic.
16. **Practice Reminders**: the things to remember to teach it.
17. **Confidence by Section**: three-column grid: Strongly Supported / Likely / Best Guess.
18. **Items to Verify Next Time**: the open questions.
19. **Signature Language**: quote box of memorable cues. No sourcing parentheticals.
20. **Pose Family Tags**: pill tags for library search.
21. **Timing Estimates**: two-column grid by section.
22. **Reconstruction Notes**: version + method, honoring the behind-the-scenes rule.

Sections 10 to 12 and 14 to 16 are include-when-useful. The rest are standard.

### Class Details Fields

```
Teacher:
Teacher Signature:
Studio:
Location:
Date / Time:
Length:
Class Type:
Level:
Lineage:             (include when known from bio)
Theme:
Method:              (the physical through-line, e.g. "opposing forces")
Peak Family:
Props:
Confidence:          (one-line summary; full grid lives in its own section)
```

### Teacher Signature (required field)

A one-line fingerprint of the teacher's recognizable trademarks: what would let someone identify
the class as theirs without a name on it. Pull from cueing voice, signature phrases, structural
habits, close rituals, and lineage. Build it from bio + observed patterns + prior reconstructions
of the same teacher. Format example:

- `[cueing tendency] · [signature pairing or theme] · [close ritual] · [breath or body emphasis]`

Keep the signature consistent and accreting across that teacher's classes.

### Mirror Table Format

A literal two-column mirror where every row says the same thing twice is duplicative noise. The
fact to convey is "every shape was done both sides," plus the few places the sides diverged.

- **Default (Option A):** single column with R+L tags. List each shape once, tag the section
  "[R + L]" or note "Both sides held the same shape order." Split into two columns only where the
  sides genuinely differed.
- **Option B (narrative asymmetry):** single-column list plus one short note beneath: "Second side
  added the bound variation; the arm balance was offered right side only."
- **Omit entirely** when the class is fully symmetric and short.

Never render a fully-duplicated two-column table.

## Voice & Formatting

- No em dashes. No AI-cadence.
- Confidence labels are per-section, never one blanket percentage.
- Reconstruct pose names from cue patterns when the teacher cues by action; keep
  Sanskrit-plus-English where it aids clarity.
- Title is the dharma, not a generic label.
- Favor strong, precise language with a soft grip: effort is allowed, force is not.
- Do not over-spiritualize. Avoid generic wellness filler. Do not flatten advanced architecture.

## Anti-Patterns

Do not:
- Reference transcripts, recordings, or audio anywhere in the output.
- Default to the full dossier when a concise flow was requested.
- Render the fully-duplicated two-column mirror table.
- Use a single blanket confidence score.
- Claim exactness from noisy input; overfit garbled words into pose names.
- Insert flashy poses because they seem plausible.
- Invent injuries, contraindications, or medical advice. General safety notes only.
- Ignore the teacher's actual pacing and voice.
- Collapse repeated flows into one round when repetition was pedagogically important.
- Leave stale references after a correction. Propagate fixes through all sections.

## Quality Check Before Answering

- Clear beginning, heat-building middle, and downshift.
- Right/left side logic is legible.
- Counts and repeats preserved if present.
- Output is shorter and cleaner than the input.
- Cue lines sound like breath-led attention, not motivational slogans.
- Confidence is honest and per-section.
- Teacher Signature is consistent with that teacher's prior classes.
- Inferred or uncertain material is named honestly.
- Never reveals how the raw material was captured.
