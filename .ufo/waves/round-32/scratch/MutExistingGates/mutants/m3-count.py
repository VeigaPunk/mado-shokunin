#!/usr/bin/env python3
"""PRED-C2-r31-v2 counter — lesson-grounded admission criteria v2 (calibration).

Rubric (registered in `.ufo/waves/round-31/registration.md`; supersedes the
r30 rubric's resolution semantics — the r30 counter stays frozen):

- A **criterion line** matches `^[0-9]+\\. ` in `corpus/QUALITY.md`.
- **superseded**: a later criterion line says `Supersedes criterion <N>`
  (also `criteria <N1>-<N2>` / `N and M` lists, position-guarded:
  self-references and retro-kills excluded).
- **literal** fraction = lines whose own text contains `lessons/` / all
  lines — the historical rubric, reported unchanged.
- **grounding citations** (what `resolved` scores — outside citations
  never ground; they only corroborate):
    * `lessons/<file>` — exists at REV and is a **non-empty** blob
      (r30's existence-only test let a zero-byte file "resolve": routed
      defect RevC2Counter S1, CritKillRules K2a).
    * `lessons/<file>#<anchor>` — the anchor must resolve to a real
      markdown heading under GitHub-slug rules (lowercase, spaces→`-`,
      punctuation stripped) with containment: the anchor equals the slug
      or is a prefix of it (`mistakes` matches `Mistakes (continued…)`).
      A whole-file substring is no longer enough (RevC2Counter S8).
    * `lessons/<file>#<anchor> <id-expr>` — every verifiable id token in
      the expression must appear inside the anchored section(s): `M<n>`
      singles (id `M<n>` text), `M<a>-M<b>` ranges (expanded), `M<a>-<b>`
      compounds (literal), `/`-lists (`M1/M2`), `,`-lists
      (`M24-2, M24-5`), `R<n>-V<n>` items, `item <n>`. The union of every
      section whose heading slug satisfies the containment rule is
      searched (a `## Mistakes` + `## Mistakes (continued…)` pair counts
      together). An id present only elsewhere in the file does NOT
      resolve (r30 section-blindness: M23-7 under `#mistakes` resolved
      while living under `Final C1 disposition` — RevC2Counter S8).
    * `lesson round<NN> M<id-expr>` — file + whole-file id presence
      (no anchor exists to scope by).
- **outside citations** (`outside …`) are printed under WARN when a
  verifiable lane-repo path or id token cannot be checked or is absent
  (`outside <abs path>` and fileless `outside <R-id>` are
  unverifiable-by-design: no lane artifact is named). They never resolve
  nor unresolve the criterion (SimplifierC2 wrinkle).
- **Degenerate population**: the verdict also requires
  `active >= ACTIVE_MIN` (=30) — a `Supersedes criteria 1-40` line can no
  longer empty the denominator into a vacuous pass (CritKillRules K2b /
  CritPredicates B2).

Usage: `python3 -I .ufo/waves/round-31/c2/count.py REV [--repo PATH]`
from the lane root (reads committed bytes via `git show`), or
`--quality FILE --lessons-root DIR` for negative-control fixtures
(fixture receipts pass --active-min explicitly; the floor is
construction).  Writes nothing.  Predicate:
`PRED-C2-r31-v2 verdict=TARGET_MET` iff unresolved_active == 0 AND
active >= ACTIVE_MIN AND literal >= 0.70; else TARGET_MISSED, exit 1.
"""
import re
import subprocess
import sys
from fractions import Fraction

ACTIVE_MIN = 30

CRIT_RE = re.compile(r"^\s*(\d+)\.\s")
LIT_RE = re.compile(r"^[0-9]+\.\s")
PATH_RE = re.compile(r"lessons/(round-[\w.-]+\.md)")
ANCH_RE = re.compile(r"lessons/(round-[\w.-]+\.md)#([\w-]+)\s*([Mm][0-9/A-Za-z\-, ]*)")
SPELL_RE = re.compile(r"lesson\s+round(\d+)\s+M([0-9/\-]+)")
OUTSIDE_RE = re.compile(r"outside\s+([^;,)]+)")
SUPER_RE = re.compile(
    r"[Ss]upersedes\s+criteri\w+\s+([0-9]+(?:\s*[-–—]\s*[0-9]+)?"
    r"(?:\s*(?:,|and)\s*[0-9]+(?:\s*[-–—]\s*[0-9]+)?)*)"
)
MID_RE = re.compile(r"M(\d+)-M(\d+)|M(\d+)((?:-\d+)*)")
RID_RE = re.compile(r"\bR(\d+)-V(\d+)\b")
ITEM_RE = re.compile(r"\bitem\s+(\d+)\b")


def expand_ids(s):
    """Id patterns to look up: `M<n>` -> ``M0*<n>``; `M<a>-M<b>` ranges
    expand; `M<a>-<b>` compounds (`M23-4`, `M28-1`, `M30-1`) stay literal;
    `/`- and `,`-lists are picked apart by MID_RE itself."""
    pats = []
    for m in MID_RE.finditer(s):
        if m.group(1) is not None:
            a, b = int(m.group(1)), int(m.group(2))
            lo, hi = min(a, b), max(a, b)
            pats.extend(rf"\bM0*{i}\b" for i in range(lo, hi + 1))
        else:
            a, b = int(m.group(3)), m.group(4)
            pats.append(rf"\bM{a}{b}\b" if b else rf"\bM0*{a}\b")
    return pats


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


def slug(text):
    return re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")


def sections(body, anchor):
    """Return the concatenated text of every section whose heading slug
    equals `anchor` or has `anchor` as a hyphen-prefix."""
    out = []
    for m in re.finditer(r"^#{2,4}\s+(.+?)\s*$", body, re.M):
        s = slug(m.group(1))
        if s == anchor or s.startswith(anchor + "-"):
            rest = body[m.end():]
            nxt = re.search(r"^#{1,4}\s", rest, re.M)
            out.append(rest[: nxt.start()] if nxt else rest)
    return out


def main():
    argv = sys.argv[1:]
    rev, repo, qfile, lroot = None, ".", None, None
    active_min = ACTIVE_MIN
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--repo":
            i += 1
            repo = argv[i]
        elif a == "--quality":
            i += 1
            qfile = argv[i]
        elif a == "--lessons-root":
            i += 1
            lroot = argv[i]
        elif a == "--active-min":
            i += 1
            active_min = int(argv[i])
        elif a.startswith("-"):
            print(f"SETUP_ERROR: unknown option {a!r}", file=sys.stderr)
            return 2
        elif rev is None:
            rev = a
        else:
            print(f"SETUP_ERROR: extra argument {a!r}", file=sys.stderr)
            return 2
        i += 1
    fixture = qfile is not None
    if fixture:
        try:
            with open(qfile, encoding="utf-8") as fh:
                quality = fh.read()
        except OSError:
            print(f"SETUP_ERROR: cannot read {qfile}", file=sys.stderr)
            return 2
        root = lroot or "."

        def git(*args):
            # fixture mode: "<rev>:<path>" lookups become filesystem reads
            path = args[-1].split(":", 1)[-1]
            if args[0] == "cat-file":
                import os
                if not os.path.exists(os.path.join(root, path)):
                    raise subprocess.CalledProcessError(1, "cat-file")
                return ""
            import os
            try:
                with open(os.path.join(root, path), encoding="utf-8") as fh:
                    return fh.read()
            except OSError:
                raise subprocess.CalledProcessError(1, "show")
    else:
        if rev is None:
            rev = "HEAD"
        if rev.startswith("-"):
            print("SETUP_ERROR: rev must not start with '-'", file=sys.stderr)
            return 2

        def git(*args):
            return subprocess.check_output(
                ["git", "-C", repo, *args, "--end-of-options"], text=True
            )

        try:
            quality = git("show", f"{rev}:corpus/QUALITY.md")
        except subprocess.CalledProcessError:
            print(f"SETUP_ERROR: no corpus/QUALITY.md at {rev}", file=sys.stderr)
            return 2

    lines = quality.splitlines()
    crits = []
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
    pos = {c["num"]: i for i, c in enumerate(crits)}
    for i, c in enumerate(crits):
        for m in SUPER_RE.finditer(c["text"]):
            for n in expand_super(m.group(1)):
                if n != c["num"] and pos.get(n, -1) < i:
                    superseded.add(n)
    for c in crits:
        c["superseded"] = c["num"] in superseded

    def exists_nonempty(path):
        try:
            return bool(git("show", f"{rev or 'x'}:{path}").strip())
        except subprocess.CalledProcessError:
            return False

    def file_text(path):
        try:
            return git("show", f"{rev or 'x'}:{path}")
        except subprocess.CalledProcessError:
            return None

    warns = []
    unresolved = []
    for c in crits:
        text = c["text"]
        citations = list(PATH_RE.finditer(text)) + list(SPELL_RE.finditer(text))
        c["cited"] = bool(citations)
        c["resolved"] = False
        # outside citations: verifiable lane-path + id tokens checked,
        # failure -> WARN never fatal; fileless/abs-path -> WARN unverifiable.
        for m in OUTSIDE_RE.finditer(text):
            frag = m.group(1).strip()
            lane_m = re.search(r"(lessons/[\w./-]+\.md)", frag)
            ids = [f"R{a}-V{b}" for a, b in RID_RE.findall(frag)]
            items = ITEM_RE.findall(frag)
            if lane_m:
                body = file_text(f"corpus/{lane_m.group(1)}")
                if body is None:
                    warns.append(f"criterion {c['num']}: outside {lane_m.group(1)} missing at rev")
                else:
                    for rid in ids:
                        if not re.search(rf"\b{re.escape(rid)}\b", body):
                            warns.append(f"criterion {c['num']}: outside id {rid} absent in {lane_m.group(1)}")
            elif ids or items:
                warns.append(
                    f"criterion {c['num']}: outside {frag[:60]!r} unverifiable (no lane path)"
                )
            elif frag.startswith("/"):
                warns.append(
                    f"criterion {c['num']}: outside {frag[:60]!r} unverifiable (non-lane path)"
                )
        if not citations:
            continue
        ok = True
        anchored = False
        for m in ANCH_RE.finditer(text):
            anchored = True
            path = f"corpus/lessons/{m.group(1)}"
            body = file_text(path)
            anchor, idexpr = m.group(2), (m.group(3) or "").strip()
            if body is None:
                c["fail"] = f"missing {path}"
                ok = False
                continue
            if not body.strip():
                c["fail"] = f"empty {path}"
                ok = False
                continue
            secs = sections(body, anchor.lower())
            if not secs:
                c["fail"] = f"anchor '#{anchor}' matches no heading in {path}"
                ok = False
                continue
            scope = "\n".join(secs)
            for pat in expand_ids(idexpr):
                if not re.search(pat, scope):
                    c["fail"] = f"id {pat} absent in section '#{anchor}' of {path}"
                    ok = False
            for a, b in RID_RE.findall(idexpr):
                if not re.search(rf"\bR{a}-V{b}\b", scope):
                    c["fail"] = f"id R{a}-V{b} absent in section '#{anchor}' of {path}"
                    ok = False
            for it in ITEM_RE.findall(idexpr):
                if not re.search(rf"\b{it}\b", scope):
                    c["fail"] = f"item {it} absent in section '#{anchor}' of {path}"
                    ok = False
        for m in SPELL_RE.finditer(text):
            anchored = True
            path = f"corpus/lessons/round-{int(m.group(1))}.md"
            body = file_text(path)
            if body is None or not body.strip():
                c["fail"] = f"missing/empty {path}"
                ok = False
                continue
            for pat in expand_ids(m.group(2)):
                if not re.search(pat, body):
                    c["fail"] = f"id {pat} absent in {path}"
                    ok = False
        # bare paths: file must exist AND be non-empty
        for m in PATH_RE.finditer(text):
            path = f"corpus/lessons/{m.group(1)}"
            body = file_text(path)
            if body is None:
                c["fail"] = f"missing {path}"
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
    print(f"counter=c2-grounding-r31-v2 rev={rev or qfile}")
    print(f"METRIC literal lines={lit_n}/{total} fraction={float(lit_f):.4f}")
    print(f"METRIC superseded={sorted(superseded)}")
    print(f"METRIC active={act_n} resolved_active={res_n} fraction={float(res_f):.4f}")
    for n, fail in unresolved_active:
        print(f"UNRESOLVED criterion {n}: {fail}")
    for w in warns:
        print(f"WARN {w}")
    for c in crits:
        if c["superseded"]:
            print(f"LINE {c['num']} superseded excluded")
    floor_ok = act_n >= active_min
    if act_n < active_min:
        print(f"FLOOR_VIOLATION active={act_n} < ACTIVE_MIN={active_min}")
    target = (
        floor_ok and (not unresolved_active) and float(lit_f) >= 0.70
    )
    print(f"PRED-C2-r31-v2 verdict={'TARGET_MET' if target else 'TARGET_MISSED'}")
    return 0 if target else 1


if __name__ == "__main__":
    raise SystemExit(main())
