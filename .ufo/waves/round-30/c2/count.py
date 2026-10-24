#!/usr/bin/env python3
"""PRED-C2-r30 counter — lesson-grounded admission criteria (calibration).

Rubric (frozen at registration, `.ufo/waves/round-30/registration.md`):

- A **criterion line** is any line of `corpus/QUALITY.md` matching
  `^[0-9]+\\. ` (the same pattern the literal r12 rubric counts).
- A criterion line is **superseded** when a later criterion line contains
  `Supersedes criterion <N>` (or `Supersedes criteria <N1>-<N2>` /
  `... N and M`), naming its number; the superseding line itself is active.
- **active** = criterion lines minus superseded ones (full supersedes only;
  criterion 21 supersedes criterion 20 by its own text).
- **literal** fraction = lines whose own text contains `lessons/` / all
  lines — the historical rubric, reported unchanged beside this counter.
- **resolved** = a criterion's text (numbered line + continuation lines) has
  at least one citation and every citation resolves:
    * `lessons/<file>` — file exists at REV;
    * `lessons/<file>#<anchor> M<id>` (also `M<a>-M<b>` ranges and
      `M<a>/M<b>` lists) — file exists and every M-id appears in that file;
    * `lesson round<NN> M<id>` (criterion-32 spelling) — mapped to
      `lessons/round-<NN>.md` plus the M-id check.
- **active_resolved** fraction = resolved active / active.
  Superseded lines are out of the denominator AND the numerator — a
  superseded ungrounded line no longer drags the active bar, and a grounded
  superseded line no longer props it.

Usage: `python3 -I .ufo/waves/round-30/c2/count.py REV` from the lane root.
Reads committed bytes via `git show`; writes nothing.  Predicate:
`PRED-C2-r30 verdict=TARGET_MET` iff every active criterion resolves
(active_resolved == 1.0000) AND literal fraction at REV >= 0.70; else
TARGET_MISSED, exit 1.  UNRESOLVED lines name each unresolved active
criterion and its failing citation.
"""
import re
import subprocess
import sys
from fractions import Fraction

CRIT_RE = re.compile(r"^\s*(\d+)\.\s")
LIT_RE = re.compile(r"^[0-9]+\.\s")
PATH_RE = re.compile(r"lessons/(round-[\w.-]+\.md)")
ANCH_RE = re.compile(r"lessons/(round-[\w.-]+\.md)#([\w-]+)\s*(M[0-9/\-]*)")
SPELL_RE = re.compile(r"lesson\s+round(\d+)\s+M([0-9/\-]+)")
# Repaired under w1 RevC2Counter S3/S4/S5/S6: the frozen rubric's grammar
# is `M<n>`, `<N1>-<N2>` and `N and M` lists, plus the observed in-repo
# spellings `M<a>-M<b>` (range) and `M<round>-<n>` (literal compound).
# A bare `M<a>-<b>` is a literal compound id (M23-4, M28-1, M30-1), never
# a numeric range — the a<=b discriminator mis-parsed the compound
# quadrant; ranges on lesson ids are spelled `M<a>-M<b>` (M01-M07).
SUPER_RE = re.compile(
    r"[Ss]upersedes\s+criteri\w+\s+([0-9]+(?:\s*[-–—]\s*[0-9]+)?"
    r"(?:\s*(?:,|and)\s*[0-9]+(?:\s*[-–—]\s*[0-9]+)?)*)"
)
MID_RE = re.compile(r"M(\d+)-M(\d+)|M(\d+)((?:-\d+)*)")


def expand_ids(s):
    """Return id patterns to look up: `M<n>` singles -> ``M0*<n>``;
    `M<a>-M<b>` ranges expand to each id; `M<a>-<b>` compounds
    (``M23-4``, ``M28-1``, ``M30-1`` — round-prefixed ids) stay literal."""
    pats = []
    for m in MID_RE.finditer(s):
        if m.group(1) is not None:
            a, b = int(m.group(1)), int(m.group(2))
            lo, hi = min(a, b), max(a, b)
            pats.extend(rf"\bM0*{i}\b" for i in range(lo, hi + 1))
        else:
            a, b = int(m.group(3)), m.group(4)
            if b:
                pats.append(rf"\bM{a}{b}\b")
            else:
                pats.append(rf"\bM0*{a}\b")
    return pats


def git(*args):
    return subprocess.check_output(["git", *args], text=True)



def expand_super(s):
    nums = []
    for part in re.split(r",|\band\b", s):
        part = part.strip()
        m = re.match(r"^(\d+)\s*[-–—]\s*(\d+)$", part)
        if m:
            nums.extend(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            nums.append(int(part))
    return nums


def main():
    rev = sys.argv[1] if len(sys.argv) > 1 else "master"
    try:
        quality = git("show", f"{rev}:corpus/QUALITY.md")
    except subprocess.CalledProcessError:
        print(f"SETUP_ERROR: no corpus/QUALITY.md at {rev}")
        return 2

    lines = quality.splitlines()
    crits = []  # (number, start_line, text incl. continuations)
    for i, line in enumerate(lines):
        m = CRIT_RE.match(line)
        if m:
            if crits:
                crits[-1]["end"] = i
            crits.append({"num": int(m.group(1)), "start": i, "end": len(lines)})
    for c in crits:
        c["text"] = "\n".join(lines[c["start"]:c["end"]])
        c["first"] = lines[c["start"]]
        c["lit"] = bool(re.match(LIT_RE, c["first"]) and "lessons/" in c["first"])

    superseded = set()
    # Rubric: "a line is superseded when a LATER line says
    # `Supersedes criterion N`" — position-guarded, self-reference and
    # retro-kills (a later row superseded by an earlier one) excluded.
    superseded = set()
    pos = {c["num"]: i for i, c in enumerate(crits)}
    for i, c in enumerate(crits):
        for m in SUPER_RE.finditer(c["text"]):
            for n in expand_super(m.group(1)):
                if n != c["num"] and pos.get(n, -1) < i:
                    superseded.add(n)
    for c in crits:
        c["superseded"] = c["num"] in superseded

    def exists(path):
        try:
            git("cat-file", "-e", f"{rev}:{path}")
            return True
        except subprocess.CalledProcessError:
            return False

    def file_text(path):
        try:
            return git("show", f"{rev}:{path}")
        except subprocess.CalledProcessError:
            return None

    unresolved = []
    for c in crits:
        text = c["text"]
        citations = list(PATH_RE.finditer(text)) + list(SPELL_RE.finditer(text))
        c["cited"] = bool(citations)
        c["resolved"] = False
        if not citations:
            continue
        ok = True
        for m in PATH_RE.finditer(text):
            path = f"corpus/lessons/{m.group(1)}"
            if not exists(path):
                c["fail"] = f"missing {path}"
                ok = False
        for m in ANCH_RE.finditer(text):
            path = f"corpus/lessons/{m.group(1)}"
            body = file_text(path)
            anchor, mids = m.group(2), m.group(3)
            if body is None:
                continue  # already flagged missing
            want = anchor.replace("-", " ")
            if want.lower() not in body.lower() and anchor.lower() not in body.lower():
                c["fail"] = f"anchor '#{anchor}' absent in {path}"
                ok = False
            for pat in expand_ids(mids or ""):
                if not re.search(pat, body):
                    c["fail"] = f"id {pat} absent in {path}"
                    ok = False
        for m in SPELL_RE.finditer(text):
            path = f"corpus/lessons/round-{int(m.group(1))}.md"
            body = file_text(path)
            if body is None:
                c["fail"] = f"missing {path}"
                ok = False
                continue
            for pat in expand_ids(m.group(2)):
                if not re.search(pat, body):
                    c["fail"] = f"id {pat} absent in {path}"
                    ok = False
        c["resolved"] = ok
    for c in crits:
        if not c["resolved"]:
            unresolved.append((c["num"], c.get("fail", "no citation")))

    total = len(crits)
    lit_n = sum(c["lit"] for c in crits)
    active = [c for c in crits if not c["superseded"]]
    act_n = len(active)
    res_n = sum(1 for c in active if c["resolved"])
    unresolved_active = [(n, f) for n, f in unresolved
                         if n in {c["num"] for c in active}]

    lit_f = Fraction(lit_n, total) if total else Fraction(0)
    res_f = Fraction(res_n, act_n) if act_n else Fraction(0)
    print(f"counter=c2-grounding-r30 rev={rev}")
    print(f"METRIC literal lines={lit_n}/{total} fraction={float(lit_f):.4f}")
    print(f"METRIC superseded={sorted(superseded)}")
    print(f"METRIC active={act_n} resolved_active={res_n} fraction={float(res_f):.4f}")
    for n, fail in unresolved_active:
        print(f"UNRESOLVED criterion {n}: {fail}")
    for c in crits:
        if not c["superseded"] and not c["resolved"]:
            continue
        if c["superseded"]:
            print(f"LINE {c['num']} superseded excluded")
    # Degenerate population guard: an empty active set is never a pass
    # (mutual supersession would print 0/0 MET otherwise).
    target = act_n > 0 and (not unresolved_active) and float(lit_f) >= 0.70
    print(f"PRED-C2-r30 verdict={'TARGET_MET' if target else 'TARGET_MISSED'}")
    return 0 if target else 1


if __name__ == "__main__":
    raise SystemExit(main())
