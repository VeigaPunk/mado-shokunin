#!/usr/bin/env python3
"""patchedcheck.py - prototype of the corrections proposed in findings.md.

Four tightenings, each re-derived with the frozen checker's own primitives:

  C1 order   - the attributed fragment's identifiers must occur in the cited
               text in the fragment's order (an unordered set lets an argument
               or operand swap through), while a dropped namespace qualifier
               still passes because only the order, not verbatim bytes, is read.
  C2 ranges  - every cited range member must be inside the file, and a reversed
               range is refused instead of normalised.
  C3 siblings- any backticked span matching LOCATOR_RE is a pointer, never a
               fact fragment, even when its name does not resolve in --fetch.
  C4 digits  - every digit run of the fragment must occur in the cited text.

A locator is OK only if all four hold; NOFRAG stays NOFRAG but is counted
separately so a caller can decide whether it is a pass.

Usage: python3 -I patchedcheck.py --fetch DIR PROSE...
"""
import argparse
import importlib.util
import os
import re
import sys

CHECKER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-locators.py"


def load_checker(path):
    spec = importlib.util.spec_from_file_location("check_locators_frozen", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(text):
    return " ".join(text.split())


def candidates(line, cl, fetch_names):
    """C3: drop every LOCATOR_RE-shaped span, resolved or not; drop bare fetch names."""
    out = []
    for m in cl.FRAG_RE.finditer(line):
        text = m.group(1)
        if cl.LOCATOR_RE.fullmatch(text.strip()) is not None:
            continue
        if cl.resolve_name(text.strip(), fetch_names) is not None:
            continue
        toks = cl.fragment_tokens(text)
        if not toks:
            continue
        out.append((m.start(), m.end(), text, toks))
    return out


def ordered_occurrence(cl, frag, text):
    """C1: the fragment's identifiers must occur in `text` in the fragment's own order."""
    pos = 0
    for tok in [t for t in cl.ID_RE.findall(frag) if len(t) >= 3]:
        pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(tok) + r"(?![A-Za-z0-9_])")
        m = pat.search(text, pos)
        if m is None:
            return False
        pos = m.end()
    return True


def range_problem(spec, nlines):
    """C2: return a reason string for a range list that references absent lines or goes backwards."""
    problems = []
    for part in spec.split(","):
        if "-" in part:
            lo_s, hi_s = part.split("-", 1)
            lo, hi = int(lo_s), int(hi_s)
            if hi < lo:
                problems.append("reversed:%s" % part)
                continue
        else:
            lo = hi = int(part)
        if lo < 1 or hi > nlines:
            problems.append("outside:%s(len=%d)" % (part, nlines))
    return ",".join(problems)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", required=True)
    ap.add_argument("prose", nargs="+")
    args = ap.parse_args(argv)
    cl = load_checker(CHECKER)
    fetch_names = {n for n in os.listdir(args.fetch) if os.path.isfile(os.path.join(args.fetch, n))}
    receipts = {}
    counts = {"loc": 0, "ok": 0, "miss": 0, "nofrag": 0, "c1": 0, "c2": 0, "c4": 0}
    for prose in args.prose:
        with open(prose, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        for lineno, line in enumerate(lines, 1):
            cands = candidates(line, cl, fetch_names)
            for m in cl.LOCATOR_RE.finditer(line):
                base = cl.resolve_name(m.group("name"), fetch_names)
                if base is None:
                    continue
                if base not in receipts:
                    receipts[base] = cl.load_receipt(os.path.join(args.fetch, base))
                lines_of = receipts[base]
                ranges = cl.parse_ranges(m.group("ranges"))
                text = cl.cited_text(lines_of, ranges)
                support = {c[2]: all(cl.token_occurs(t, text) for t in c[3]) for c in cands}
                before = [c for c in cands if c[1] <= m.start()]
                after = [c for c in cands if c[0] >= m.end()]
                attr = before[-1] if before else (after[0] if after else None)
                counts["loc"] += 1
                if attr is None:
                    counts["nofrag"] += 1
                    print("PATCHED %s:%d %s verdict=NOFRAG" % (prose, lineno, m.group(0)))
                    continue
                frag = attr[2]
                reasons = []
                if not ordered_occurrence(cl, frag, text):
                    reasons.append("C1-order")
                    counts["c1"] += 1
                bad = range_problem(m.group("ranges"), len(lines_of))
                if bad:
                    reasons.append("C2-range:" + bad)
                    counts["c2"] += 1
                missing = [n for n in re.findall(r"[0-9]+", frag)
                           if not re.search(r"(?<![0-9])" + re.escape(n) + r"(?![0-9])", text)]
                if missing:
                    reasons.append("C4-digits:" + ",".join(missing))
                    counts["c4"] += 1
                verdict = "OK" if (support[attr[2]] and not reasons) else "MISS"
                counts["ok" if verdict == "OK" else "miss"] += 1
                print("PATCHED %s:%d %s verdict=%s why=%s attr=%r"
                      % (prose, lineno, m.group(0), verdict, ";".join(reasons) or "supported", frag))
    print("PATCHED_TOTAL locators=%d ok=%d miss=%d nofrag=%d c1_quote=%d c2_range=%d c4_digits=%d"
          % (counts["loc"], counts["ok"], counts["miss"], counts["nofrag"],
             counts["c1"], counts["c2"], counts["c4"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
