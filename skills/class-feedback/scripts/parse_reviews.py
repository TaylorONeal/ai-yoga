"""Parse a pile of pasted yoga-class reviews into structured signal.

This is a preprocessing aid for the `class-feedback` "reviews digest" mode. It
does the mechanical sorting so the human read can focus on judgment: it splits a
blob of pasted reviews into individual entries, pulls a star rating out of each
where one is present, separates teaching feedback from non-teaching complaints
(temperature, price, parking, the app, the front desk), buckets recurring themes,
and flags single-occurrence notes as outliers.

It does NOT write the digest and it does NOT decide what the teacher should do.
It weighs and sorts; a person reads the result for the need underneath the words.
Never paste this JSON at a teacher as if it were feedback. See
`references/reading-reviews.md` for how to turn the buckets into a usable read.

Pure standard library — no dependencies. Python 3.8+.

Usage:
    python scripts/parse_reviews.py reviews.txt
    python scripts/parse_reviews.py reviews.txt --output parsed.json
    pbpaste | python scripts/parse_reviews.py -            # read from stdin

Input format:
    One review per block, blocks separated by a blank line or a line of `---`.
    A rating anywhere in a block is picked up: "5 stars", "5/5", "Rating: 4",
    "★★★★☆", or a leading "5 -". Blocks without a rating are still parsed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# --- Theme taxonomy -------------------------------------------------------
#
# Each theme maps a cluster of surface phrases to the NEED underneath, per the
# "translate the complaint into the need" rule. `polarity` is the direction the
# theme usually points when it shows up: "praise" themes are strengths students
# name, "issue" themes are the actionable complaints. A single review can hit
# several themes.

TEACHING_THEMES = [
    {
        "key": "pacing_talking",
        "label": "Pacing / too much talking",
        "need": "Less standing around, more moving or tighter cueing.",
        "polarity": "issue",
        "patterns": [
            r"too much talk", r"talked too much", r"talk(s|ed|ing)? a lot",
            r"stood around", r"standing around", r"long.?winded", r"rambl",
            r"too slow", r"dragged", r"lost momentum", r"waiting around",
        ],
    },
    {
        "key": "clarity_lost",
        "label": "Cue clarity / felt lost",
        "need": "Clearer cues and sign-posting; pacing that lets people follow.",
        "polarity": "issue",
        "patterns": [
            r"felt lost", r"got lost", r"confus", r"hard to follow",
            r"couldn'?t follow", r"didn'?t know what", r"unclear", r"vague cue",
            r"no idea what", r"lost track",
        ],
    },
    {
        "key": "intensity_low",
        "label": "Not a real workout / intensity",
        "need": "The challenge or intensity sign-posting was unclear.",
        "polarity": "issue",
        "patterns": [
            r"not a (real )?workout", r"not challenging", r"too easy",
            r"barely broke a sweat", r"wanted more", r"not enough", r"too gentle",
            r"expected (more|harder)",
        ],
    },
    {
        "key": "too_hard_options",
        "label": "Too hard / missing options",
        "need": "Options and modifications were missing, not that the plan was wrong.",
        "polarity": "issue",
        "patterns": [
            r"too hard", r"too advanced", r"too difficult", r"couldn'?t keep up",
            r"no modif", r"no option", r"not for beginners", r"over my head",
            r"felt behind",
        ],
    },
    {
        "key": "adjustments",
        "label": "Hands-on adjustments",
        "need": "Consent and calibration of physical assists.",
        "polarity": "mixed",
        "patterns": [
            r"adjust", r"hands.?on", r"touch(ed|ing)?", r"assist(s|ed|ing)?",
            r"pushed too", r"correction",
        ],
    },
    {
        "key": "sequencing",
        "label": "Sequencing / flow",
        "need": "How the arc was built and whether the peak was earned.",
        "polarity": "praise",
        "patterns": [
            r"sequenc", r"great flow", r"nice flow", r"well.?built",
            r"thoughtful (class|sequence|flow)", r"creative (flow|sequence)",
            r"smooth transition", r"well.?structured", r"built (up|nicely)",
        ],
    },
    {
        "key": "cueing_good",
        "label": "Cueing (positive)",
        "need": "Clear, well-timed instruction that students could act on.",
        "polarity": "praise",
        "patterns": [
            r"clear cue", r"great cue", r"cued (well|beautifully|clearly)",
            r"easy to follow", r"clear instruction", r"well explained",
            r"great instruction",
        ],
    },
    {
        "key": "theme_intention",
        "label": "Theme / intention",
        "need": "Whether the class's idea got taught, not just announced.",
        "polarity": "praise",
        "patterns": [
            r"theme", r"intention", r"meaningful", r"philosophy", r"message",
            r"spiritual", r"grounding", r"centered? me", r"left feeling",
        ],
    },
    {
        "key": "atmosphere_warmth",
        "label": "Warmth / atmosphere",
        "need": "How the room felt; whether students felt welcomed and seen.",
        "polarity": "praise",
        "patterns": [
            r"welcoming", r"warm", r"kind", r"friendly", r"inclusive",
            r"felt seen", r"felt safe", r"encourag", r"supportive", r"held space",
            r"great energy", r"positive energy",
        ],
    },
    {
        "key": "music",
        "label": "Music / playlist",
        "need": "Soundtrack fit and volume.",
        "polarity": "mixed",
        "patterns": [
            r"music", r"playlist", r"song", r"too loud", r"soundtrack",
        ],
    },
    {
        "key": "voice_presence",
        "label": "Voice / teaching presence",
        "need": "The teacher's delivery, tone, and command of the room.",
        "polarity": "praise",
        "patterns": [
            r"great teacher", r"amazing teacher", r"wonderful instructor",
            r"calming voice", r"soothing voice", r"presence", r"knowledgeable",
            r"best teacher", r"favorite (teacher|instructor)", r"loved (the )?instructor",
        ],
    },
]

# Non-teaching complaints: real, but not feedback on the teaching. Set aside.
NON_TEACHING_THEMES = [
    {
        "key": "temperature",
        "label": "Room temperature",
        "patterns": [r"too hot", r"too cold", r"temperature", r"freezing", r"sweltering", r"a\/c", r"air condition", r"heat(ing)? (was|wasn'?t)"],
    },
    {
        "key": "price",
        "label": "Price / value",
        "patterns": [r"too expensive", r"overpriced", r"price", r"\$\d", r"cost too", r"not worth the money", r"pricey"],
    },
    {
        "key": "parking",
        "label": "Parking / location",
        "patterns": [r"parking", r"hard to find", r"no parking", r"location was"],
    },
    {
        "key": "booking_app",
        "label": "App / booking",
        "patterns": [r"app (crash|kept|wouldn|is)", r"booking", r"website", r"couldn'?t sign up", r"waitlist", r"check.?in (was|process)"],
    },
    {
        "key": "front_desk",
        "label": "Front desk / staff",
        "patterns": [r"front desk", r"reception", r"staff (was|were) rude", r"unfriendly staff", r"greeted"],
    },
    {
        "key": "facilities",
        "label": "Facilities / cleanliness",
        "patterns": [r"dirty", r"clean", r"bathroom", r"locker", r"shower", r"smell(ed|y)", r"mats were", r"crowded", r"too packed", r"overbooked", r"no room", r"props"],
    },
]

POSITIVE_WORDS = re.compile(
    r"\b(love|loved|great|amazing|wonderful|excellent|best|favorite|fantastic|"
    r"awesome|perfect|highly recommend|beautiful|incredible|nourishing|"
    r"transformative|the best)\b", re.I)
NEGATIVE_WORDS = re.compile(
    r"\b(disappoint|worst|awful|terrible|bad|hate|hated|never again|waste|"
    r"rude|boring|frustrat|annoy|wouldn'?t recommend|not great|meh|underwhelm)\b", re.I)

RATING_PATTERNS = [
    re.compile(r"(\d(?:\.\d)?)\s*(?:out of|/)\s*5", re.I),
    re.compile(r"(\d(?:\.\d)?)\s*star", re.I),
    re.compile(r"rating[:\s]+(\d(?:\.\d)?)", re.I),
    re.compile(r"^\s*(\d(?:\.\d)?)\s*[-–—:]", re.I),
]
STAR_GLYPHS = re.compile(r"[★⭐]")


def split_reviews(text: str):
    """Split a blob into individual review blocks.

    Prefer explicit `---` separators; else split on blank lines.
    """
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    if re.search(r"^\s*-{3,}\s*$", text, re.M):
        blocks = re.split(r"^\s*-{3,}\s*$", text, flags=re.M)
    else:
        blocks = re.split(r"\n\s*\n", text)
    return [b.strip() for b in blocks if b.strip()]


def extract_rating(block: str):
    for pat in RATING_PATTERNS:
        m = pat.search(block)
        if m:
            try:
                val = float(m.group(1))
                if 0 <= val <= 5:
                    return val
            except ValueError:
                pass
    glyphs = STAR_GLYPHS.findall(block)
    if 1 <= len(glyphs) <= 5:
        return float(len(glyphs))
    return None


def match_themes(block: str, themes):
    hits = []
    for theme in themes:
        for pat in theme["patterns"]:
            if re.search(pat, block, re.I):
                hits.append(theme["key"])
                break
    return hits


def sentiment(block: str, rating):
    if rating is not None:
        if rating >= 4:
            return "positive"
        if rating <= 2:
            return "negative"
        return "mixed"
    pos = len(POSITIVE_WORDS.findall(block))
    neg = len(NEGATIVE_WORDS.findall(block))
    if pos and neg:
        return "mixed"
    if pos:
        return "positive"
    if neg:
        return "negative"
    return "neutral"


def parse(text: str):
    blocks = split_reviews(text)
    theme_by_key = {t["key"]: t for t in TEACHING_THEMES}
    non_teaching_by_key = {t["key"]: t for t in NON_TEACHING_THEMES}

    reviews = []
    for i, block in enumerate(blocks, 1):
        rating = extract_rating(block)
        teaching_hits = match_themes(block, TEACHING_THEMES)
        non_teaching_hits = match_themes(block, NON_TEACHING_THEMES)
        reviews.append({
            "index": i,
            "rating": rating,
            "sentiment": sentiment(block, rating),
            "teaching_themes": teaching_hits,
            "non_teaching_themes": non_teaching_hits,
            "chars": len(block),
        })

    ratings = [r["rating"] for r in reviews if r["rating"] is not None]
    teaching_counter = Counter(k for r in reviews for k in r["teaching_themes"])
    non_teaching_counter = Counter(k for r in reviews for k in r["non_teaching_themes"])

    # Patterns vs outliers: a theme in 2+ reviews is a pattern worth weighing;
    # a theme in exactly one review is an outlier to note, not act on.
    def theme_rows(counter, lookup, want_polarity=None):
        rows = []
        for key, count in counter.most_common():
            t = lookup[key]
            if want_polarity and t.get("polarity") not in want_polarity:
                continue
            rows.append({
                "key": key,
                "label": t["label"],
                "need": t.get("need", ""),
                "count": count,
                "is_pattern": count >= 2,
            })
        return rows

    teaching_rows = theme_rows(teaching_counter, theme_by_key)
    issue_patterns = [r for r in teaching_rows
                      if r["is_pattern"] and theme_by_key[r["key"]]["polarity"] in ("issue", "mixed")]
    praise_patterns = [r for r in teaching_rows
                       if r["is_pattern"] and theme_by_key[r["key"]]["polarity"] in ("praise", "mixed")]

    # "The one pattern worth acting on" candidate: most frequent issue pattern.
    one_to_act_on = issue_patterns[0] if issue_patterns else None

    sentiments = Counter(r["sentiment"] for r in reviews)

    return {
        "summary": {
            "total_reviews": len(reviews),
            "rated_reviews": len(ratings),
            "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else None,
            "sentiment_breakdown": dict(sentiments),
        },
        "teaching_signal": {
            "praise_patterns": praise_patterns,
            "issue_patterns": issue_patterns,
            "one_pattern_worth_acting_on": one_to_act_on,
            "all_themes": teaching_rows,
        },
        "set_aside_non_teaching": theme_rows(non_teaching_counter, non_teaching_by_key),
        "outliers": [
            {"key": r["key"], "label": r["label"], "count": r["count"]}
            for r in teaching_rows if not r["is_pattern"]
        ],
        "reviews": reviews,
        "_note": (
            "Preprocessing only. Read teaching_signal for the need underneath the "
            "words; weigh issue_patterns (2+ reviews) over outliers. Set-aside items "
            "are facilities/price/app, not teaching. Do not paste this at a teacher."
        ),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="Path to a text file of reviews, or - for stdin")
    ap.add_argument("--output", "-o", help="Write JSON here (default: stdout)")
    args = ap.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.input).read_text(encoding="utf-8")

    result = parse(text)
    out = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(out + "\n", encoding="utf-8")
        s = result["summary"]
        print(f"Wrote {args.output}")
        print(f"  {s['total_reviews']} reviews · avg {s['avg_rating']} "
              f"({s['rated_reviews']} rated) · {s['sentiment_breakdown']}")
        issues = result["teaching_signal"]["issue_patterns"]
        if issues:
            print("  Issue patterns:", ", ".join(f"{r['label']} (×{r['count']})" for r in issues))
        set_aside = result["set_aside_non_teaching"]
        if set_aside:
            print("  Set aside:", ", ".join(f"{r['label']} (×{r['count']})" for r in set_aside))
    else:
        print(out)


if __name__ == "__main__":
    main()
