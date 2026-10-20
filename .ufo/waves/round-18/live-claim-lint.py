#!/usr/bin/env python3
"""live-claim-lint.py — flag present-tense live-behaviour claims in documentary notes.

Scope: the corpus/knowledge notes that open with "Documentary route only" —
the upstream contract and the host file bytes are read, never observed. In
such a note a present-tense sentence asserting what the host is doing is a
claim that needs either a verbatim upstream quote (quotes/backticks plus a
file/line anchor) or an inference/unknown/declared tag.

Flagged lexical families (case-insensitive, one hit per line):
  copula-state  is/are [currently|now|still|already|not|no longer]*
                running|displaying|showing|active|loaded|listening|visible|
                open|mounted|alive
  dynamic       reload(s|ed|ing), relaunch(es|ed|ing), launch(es|ed|ing),
                fire(s|d|ing)
  live-now      "right now"
  observation   observed, displays
  perfect       has/have loaded|reloaded|relaunched|launched|started|fired|
                spawned

Not flagged on purpose (the corpus uses these overwhelmingly to describe
source code and they are outside the item's lexical set): bare runs / starts /
spawns / restarts / reads / writes / opens / exits.

Exemptions, first match wins:
  marker    the line carries [UNK]/[INF]/[INF-docs]/[OBS, bytes], or
            documentary vocabulary: declared*, documentary, documented,
            documentation, according to, from source, source-side, in code,
            from code, read as bytes, bytes only, byte read, host bytes.
  quote     the match lies inside a double-quoted, curly-quoted or backticked
            span AND its paragraph carries a file/line anchor ([WR:59],
            README.md:100-101, HC:289, alacritty.5.scd:31). Verbatimness is
            not checked; the anchor is the proxy.
  negated   a negator (not|never|no|without|neither|nor|cannot|n't) appears
            in the same sentence BEFORE the match. A negated copula inside
            the match ("is not running") is still a live-state claim and is
            reported.
  question  the sentence is interrogative: contains "?" or a "whether"
            clause before the match.

Not scanned: everything before the first level-1 heading (the
source:/verified-at metadata header), everything from `## Unexercised
behavior` to the next level-1/2 heading, and fenced code blocks.

Output, one line per file:
    NOTE <path as given> clean|HITS scanned=<n> hits=<n>
then one line per hit:
    LINE <path as given>:<n> <stripped line text>
then one summary line across all files:
    SUMMARY files=N scanned=N candidates=N hits=H exempt_marker=N
            exempt_quote=N exempt_negated=N exempt_question=N
--explain adds `  match=<family> phrase=<repr>` after each hit and an
`EXEMPT <path>:<n> <reason> <repr phrase>` line for every suppressed
candidate (useful when judging whether an exemption was right).

Exit: 0 no hit; 1 at least one hit; 2 usage or read error. --selftest runs
built-in fixtures (clean note, live claim, quote with/without anchor, marker,
disclaimer negation, interrogative, negative copula, right now, question,
excluded section, front matter, fence) and exits 0/1.
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

EXCLUDED_HEADING = re.compile(r"^##\s+Unexercised\s+behaviou?r\s*$", re.I)
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s")
TITLE = re.compile(r"^\s{0,3}#\s")
FENCE = re.compile(r"^\s{0,3}(?:```|~~~)")
NEW_BLOCK = re.compile(r"^\s{0,3}(?:[-*+]\s|\d+[.)]\s|\||>)")

CLAIM_PATTERNS = (
    (
        "copula-state",
        re.compile(
            r"\b(?:is|are)\s+"
            r"(?:(?:currently|now|still|already|not|no\s+longer)\s+)*"
            r"(?:running|displaying|showing|active|loaded|listening|"
            r"visible|open|mounted|alive)\b",
            re.I,
        ),
    ),
    (
        "dynamic",
        re.compile(
            r"\b(?:reloads|reloaded|reloading|relaunches|relaunched|"
            r"relaunching|launches|launched|launching|fires|fired|firing)\b",
            re.I,
        ),
    ),
    ("live-now", re.compile(r"\bright\s+now\b", re.I)),
    ("observation", re.compile(r"\bobserved\b|\bdisplays\b", re.I)),
    (
        "perfect",
        re.compile(
            r"\b(?:has|have)\s+"
            r"(?:loaded|reloaded|relaunched|launched|started|fired|spawned)\b",
            re.I,
        ),
    ),
)

# `[WR:59]`, `[HC:104-107]`, `[WM:104-105, 782]`, `README.md:100-101`,
# `alacritty.5.scd:31`, `HC:289`. The bare form must end with a letter or a
# dot before the colon so a timestamp like `T09:16` is not an anchor.
ANCHOR_RE = re.compile(
    r"\[[A-Za-z][A-Za-z0-9]{0,7}:\d+(?:[-,]\s*\d+(?:-\d+)?)*\]"
    r"|\b[A-Za-z][\w./-]*[A-Za-z.]:\d+(?:[-,]\s*\d+(?:-\d+)?)*"
)

DOC_MARKER_RE = re.compile(
    r"\[UNK\]|\[INF[^\]]*\]|\bUNK\b|\bINF\b"
    r"|\bdeclared\b|\bdeclares\b|\bdeclaration\b|\bdeclarations\b"
    r"|\bdocumentary\b|\bdocumented\b|\bdocuments?\b|\bdocumentation\b"
    r"|\baccording to\b"
    r"|\bfrom source\b|\bsource-side\b|\bin code\b|\bfrom code\b"
    r"|\bread as bytes\b|\bbytes only\b|\bbyte read\b|\bhost bytes\b"
    r"|\[OBS,\s*bytes\]",
    re.I,
)

# Sentence boundaries: . ! ? ; followed by whitespace (line wraps included),
# minus the common abbreviations. Newlines alone are not boundaries.
BOUNDARY = re.compile(
    r"(?<!\be\.g)(?<!\bi\.e)(?<!\bcf)(?<!\bvs)[.!?;](?=\s)"
)
NEGATOR = re.compile(
    r"\b(?:not|never|no|without|neither|nor|cannot|unobserved)\b|n't\b", re.I
)
INTERROGATIVE = re.compile(r"\bwhether\b", re.I)


def quote_regions(text):
    """Return [(start, end), ...] spans of quoted/backticked text in a paragraph."""
    regions = []
    simple = {'"': False, "`": False}
    starts = {'"': 0, "`": 0}
    curly_open = None
    for i, ch in enumerate(text):
        if ch in simple:
            if simple[ch]:
                regions.append((starts[ch], i + 1))
                simple[ch] = False
            else:
                simple[ch] = True
                starts[ch] = i
        elif ch == "\u201c":
            if curly_open is None:
                curly_open = i
        elif ch == "\u201d":
            if curly_open is not None:
                regions.append((curly_open, i + 1))
                curly_open = None
    for delim, opened in simple.items():
        if opened:
            regions.append((starts[delim], len(text)))
    if curly_open is not None:
        regions.append((curly_open, len(text)))
    return regions


def sentences(text):
    """Yield (start, end) sentence spans of a paragraph."""
    start = 0
    for m in BOUNDARY.finditer(text):
        if m.start() > start:
            yield start, m.start() + 1
        start = m.end()
    if start < len(text):
        yield start, len(text)


def sentence_span(text, pos):
    for start, end in sentences(text):
        if start <= pos < end:
            return start, end
    return 0, len(text)


def line_starts(texts):
    starts = []
    off = 0
    for t in texts:
        starts.append(off)
        off += len(t) + 1
    return starts


def offset_line(starts, pos):
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= pos:
            lo = mid
        else:
            hi = mid - 1
    return lo


def is_quoted(regions, pos):
    return any(lo <= pos < hi for lo, hi in regions)


def classify(paragraph):
    """Yield (index, line_text, family, phrase, verdict, reason) per match.

    `index` is the paragraph-relative line index; lint_text maps it to the
    file line number through the paragraph's (file_idx, text) pairs.
    """
    texts = [t for _, t in paragraph]
    joined = "\n".join(texts)
    regions = quote_regions(joined)
    has_anchor = ANCHOR_RE.search(joined) is not None
    starts = line_starts(texts)
    for family, rx in CLAIM_PATTERNS:
        for m in rx.finditer(joined):
            pos = m.start()
            li = offset_line(starts, pos)
            line_text = texts[li]
            phrase = m.group(0)
            if DOC_MARKER_RE.search(line_text):
                yield li, line_text, family, phrase, "exempt", "marker"
                continue
            if has_anchor and is_quoted(regions, pos):
                yield li, line_text, family, phrase, "exempt", "quote"
                continue
            s_start, s_end = sentence_span(joined, pos)
            before = joined[s_start:pos]
            sentence = joined[s_start:s_end]
            if NEGATOR.search(before):
                yield li, line_text, family, phrase, "exempt", "negated"
                continue
            if "?" in sentence or INTERROGATIVE.search(before):
                yield li, line_text, family, phrase, "exempt", "question"
                continue
            yield li, line_text, family, phrase, "hit", ""


def scan(text):
    """Walk one note; yield HEADING/paragraph events with their line indices."""
    lines = text.splitlines()
    in_front = True
    in_fence = False
    excluded = False
    paragraph = []

    def flush():
        nonlocal paragraph
        if paragraph:
            yield paragraph
            paragraph = []

    for idx, line in enumerate(lines):
        if in_front:
            if TITLE.match(line):
                in_front = False
            else:
                continue
        if FENCE.match(line):
            yield from flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING.match(line)
        if m:
            yield from flush()
            level = len(m.group(1))
            if level == 2 and EXCLUDED_HEADING.match(line):
                excluded = True
            elif level <= 2:
                excluded = False
            if not excluded:
                yield [(idx, line)]
            continue
        if excluded:
            continue
        if not line.strip():
            yield from flush()
            continue
        if NEW_BLOCK.match(line) and paragraph:
            yield from flush()
        paragraph.append((idx, line))
    yield from flush()


def lint_text(text):
    hits = []
    exempt = []
    counts = {
        "scanned": 0,
        "candidates": 0,
        "exempt_marker": 0,
        "exempt_quote": 0,
        "exempt_negated": 0,
        "exempt_question": 0,
    }
    seen = set()
    for paragraph in scan(text):
        counts["scanned"] += len(paragraph)
        for li, line_text, family, phrase, verdict, reason in classify(paragraph):
            lineno = paragraph[li][0] + 1
            counts["candidates"] += 1
            if verdict == "hit":
                if lineno not in seen:
                    seen.add(lineno)
                    hits.append((lineno, line_text, family, phrase))
            else:
                counts[f"exempt_{reason}"] += 1
                exempt.append((lineno, family, phrase, reason))
    return hits, exempt, counts


def read_source(arg):
    if arg == "-":
        return "<stdin>", sys.stdin.read()
    path = Path(arg)
    try:
        return arg, path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"live-claim-lint: cannot read {arg}: {exc}", file=sys.stderr)
        sys.exit(2)


SELFTEST_CASES = [
    (
        "clean",
        [],
        """source: fixture
verified-at: today

# Fixture — documentary

Documentary route only. The service was not observed running.

## Contract

- `main.c:9`: "the daemon is running"
- [UNK] whether the socket is open
- declared value only: the socket is open
- `hypridle.conf:2` `lock_cmd = omarchy-system-lock`

## Unexercised behavior

- [UNK] whether the daemon is running now
""",
    ),
    (
        "dirty-present-tense",
        [5, 6, 7],
        """source: fixture

# Fixture

swaybg is running now.
The launcher reloads its theme.
That behaviour was observed on this host.

## Unexercised behavior

- [UNK] whether swaybg is running.
""",
    ),
    (
        "quote-without-anchor",
        [3],
        """# Fixture

He said "the service is running" in the meeting.
""",
    ),
    (
        "quote-with-anchor",
        [],
        """# Fixture

`README.md:5` states: "the service is running".
""",
    ),
    (
        "backtick-with-anchor",
        [],
        """# Fixture

- `main.c:12` — `the daemon is running`
""",
    ),
    (
        "markers",
        [],
        """# Fixture

- [UNK] the daemon is running.
- [INF] the daemon is running.
- declared only: the daemon is running.
- documentary: the daemon is running.
""",
    ),
    (
        "negated-disclaimer",
        [],
        """# Fixture

No consumer was reloaded, and the process was not observed running.
""",
    ),
    (
        "interrogative",
        [],
        """# Fixture

Whether swaybg is running is unknown.
""",
    ),
    (
        "negative-copula",
        [3],
        """# Fixture

Swaybg is not running.
""",
    ),
    (
        "right-now",
        [3],
        """# Fixture

Right now the compositor draws the wallpaper.
""",
    ),
    (
        "question-mark",
        [],
        """# Fixture

The daemon is running — or is it?
""",
    ),
    (
        "front-matter",
        [],
        """source: swaybg is running

# Fixture

Body with nothing to flag.
""",
    ),
    (
        "fenced",
        [],
        """# Fixture

```
swaybg is running
```
""",
    ),
]


def run_selftest():
    ok = 0
    with tempfile.TemporaryDirectory(prefix="live-claim-lint-") as tmp:
        for name, want, text in SELFTEST_CASES:
            path = Path(tmp) / f"{name}.md"
            path.write_text(text, encoding="utf-8")
            hits, _exempt, _counts = lint_text(path.read_text(encoding="utf-8"))
            got = sorted({h[0] for h in hits})
            good = got == want
            ok += good
            state = "PASS" if good else "FAIL"
            print(
                f"SELFTEST {name} {state} want={want} got={got}"
                + (
                    ""
                    if good
                    else " " + repr([(h[0], h[1].strip()) for h in hits])
                )
            )
    total = len(SELFTEST_CASES)
    print(f"SELFTEST {ok}/{total}")
    return 0 if ok == total else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Flag present-tense live-behaviour claims in documentary "
        "corpus/knowledge notes."
    )
    ap.add_argument("notes", nargs="*", help="note path(s); `-` reads stdin")
    ap.add_argument(
        "--selftest",
        action="store_true",
        help="run built-in fixtures instead of scanning files",
    )
    ap.add_argument(
        "--explain",
        action="store_true",
        help="show the matched family/phrase and every exemption",
    )
    args = ap.parse_args(argv)

    if args.selftest:
        return run_selftest()

    if not args.notes:
        ap.error("at least one note path is required (or --selftest)")

    totals = {
        "files": 0,
        "scanned": 0,
        "candidates": 0,
        "hits": 0,
        "exempt_marker": 0,
        "exempt_quote": 0,
        "exempt_negated": 0,
        "exempt_question": 0,
    }
    for arg in args.notes:
        label, text = read_source(arg)
        hits, exempt, counts = lint_text(text)
        totals["files"] += 1
        for key, value in counts.items():
            totals[key] += value
        role = "HITS" if hits else "clean"
        print(f"NOTE {label} {role} scanned={counts['scanned']} hits={len(hits)}")
        for lineno, line_text, family, phrase in hits:
            print(f"LINE {label}:{lineno} {line_text.strip()}")
            if args.explain:
                print(f"  match={family} phrase={phrase!r}")
        if args.explain:
            for lineno, family, phrase, reason in exempt:
                print(f"EXEMPT {label}:{lineno} {reason} {phrase!r}")
        totals["hits"] += len(hits)

    print(
        "SUMMARY "
        f"files={totals['files']} scanned={totals['scanned']} "
        f"candidates={totals['candidates']} hits={totals['hits']} "
        f"exempt_marker={totals['exempt_marker']} "
        f"exempt_quote={totals['exempt_quote']} "
        f"exempt_negated={totals['exempt_negated']} "
        f"exempt_question={totals['exempt_question']}"
    )
    return 1 if totals["hits"] else 0


if __name__ == "__main__":
    sys.exit(main())
