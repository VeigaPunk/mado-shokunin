#!/usr/bin/env python3
"""Build the extra single-defect mutant population for C1 (round 44, seat ExecC1ExtraMutants).

Each mutant is a list of (old, new) text replacements applied to the reference
(.ufo/waves/round-44/c1/ctl-ref-tool.py.txt); every replacement must match exactly once,
else the build aborts. Bodies are written to the seat dir (mutants/) and a manifest is
printed: name, note, sha256, changed-line count.

Usage: python3 build.py
"""
import hashlib
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF = os.path.join(LANE, ".ufo/waves/round-44/c1/ctl-ref-tool.py.txt")
SEAT = os.path.join(LANE, ".ufo/waves/round-44/w1/ExecC1ExtraMutants/mutants")

A1 = "isinstance(f, int) and not isinstance(f, bool) and f in (1, 2)"
RET = '        return f\n    return 0\n'
KEY = '    f = c.get("fullscreen")\n'
FS_BR = '        elif fsmode == 2:\n            verdict = "FULLSCREEN"\n'
MAX_BR = '        elif fsmode == 1:\n            verdict = "MAXIMIZED"\n'
TALLY = '        tally[verdict.lower()] += 1\n'
UNMAPPED = ('        if c.get("mapped") is False:\n'
            '            tally["unmapped"] += 1\n'
            '            continue\n')
NOMATCH = '        if want is None:\n            continue\n'
SUFFIX = '    if t["maximized"] + t["fullscreen"] > 0:\n'
STATES = '        states = " maximized=%d fullscreen=%d" % (t["maximized"], t["fullscreen"])\n'
FMT = '"matched=%d unmapped=%d agree=%d differ=%d tiled=%d badsize=%d%s verdict=%s" % ('
ARGS = 't["tiled"], t["badsize"], states, verdict))'
CHAIN = ('        if size is None:\n'
         '            verdict = "BADSIZE"\n'
         '        elif fsmode == 2:\n'
         '            verdict = "FULLSCREEN"\n'
         '        elif fsmode == 1:\n'
         '            verdict = "MAXIMIZED"\n')

SPEC = [
    # ---- client_fsmode: boundary / membership (defects)
    ("M01-fsmode-extra-3", "membership admits 3 (boundary: extra value)", [
        (A1, "isinstance(f, int) and not isinstance(f, bool) and f in (1, 2, 3)")]),
    ("M02-fsmode-drop-2", "membership drops fullscreen 2", [
        (A1, "isinstance(f, int) and not isinstance(f, bool) and f in (1,)")]),
    ("M03-fsmode-only-2", "membership keeps only 2 (drops maximized 1)", [
        (A1, "isinstance(f, int) and not isinstance(f, bool) and f in (2,)")]),
    ("M04-fsmode-admit-0", "membership admits 0", [
        (A1, "isinstance(f, int) and not isinstance(f, bool) and f in (0, 1, 2)")]),
    ("M05-fsmode-admit-neg", "membership admits -1", [
        (A1, "isinstance(f, int) and not isinstance(f, bool) and f in (-1, 1, 2)")]),
    ("M06-fsmode-range-chain", "membership as chained compare 1 <= f <= 2", [
        (A1, "isinstance(f, int) and not isinstance(f, bool) and 1 <= f <= 2")]),
    ("M07-fsmode-set-literal", "membership as set literal (unhashable values raise)", [
        ("not isinstance(f, bool) and f in (1, 2)",
         "not isinstance(f, bool) and f in {1, 2}")]),
    # ---- client_fsmode: type guard
    ("M08-drop-int-guard", "int guard dropped (floats 2.0 admitted)", [
        (A1, "not isinstance(f, bool) and f in (1, 2)")]),
    ("M09-guard-int-or-bool", "int guard widened to (int, bool)", [
        (A1, "isinstance(f, (int, bool)) and not isinstance(f, bool) and f in (1, 2)")]),
    ("M10-guard-type-is", "isinstance int guard -> type(f) is int", [
        (A1, "type(f) is int and not isinstance(f, bool) and f in (1, 2)")]),
    ("M11-guard-type-not-bool", "bool guard as type(f) is not bool", [
        (A1, "isinstance(f, int) and type(f) is not bool and f in (1, 2)")]),
    ("M12-guard-is-not-true", "bool guard as f is not True and f is not False", [
        (A1, "isinstance(f, int) and f is not True and f is not False and f in (1, 2)")]),
    ("M13-guard-float-reject", "bool guard replaced by not isinstance(f, float) (bools pass)", [
        (A1, "isinstance(f, int) and not isinstance(f, float) and f in (1, 2)")]),
    ("M14-guard-float-only", "int guard replaced by float guard", [
        (A1, "isinstance(f, float) and f in (1, 2)")]),
    ("M15-guard-float-admit", "int guard widened to (int, float), return unchanged", [
        (A1, "isinstance(f, (int, float)) and not isinstance(f, bool) and f in (1, 2)")]),
    ("M16-conjunct-reorder", "conjuncts reordered (membership first)", [
        (A1, "f in (1, 2) and not isinstance(f, bool) and isinstance(f, int)")]),
    ("M17-membership-str", "membership by str(f) in ('1','2')", [
        (A1, "isinstance(f, int) and not isinstance(f, bool) and str(f) in (\"1\", \"2\")")]),
    # ---- client_fsmode: return value / key
    ("M18-return-bool", "returns bool(f)", [
        (RET, '        return bool(f)\n    return 0\n')]),
    ("M19-return-ternary", "returns 2 if f == 2 else 1", [
        (RET, '        return 2 if f == 2 else 1\n    return 0\n')]),
    ("M20-return-min", "returns min(f, 2)", [
        (RET, '        return min(f, 2)\n    return 0\n')]),
    ("M21-return-mod", "returns f % 3", [
        (RET, '        return f % 3\n    return 0\n')]),
    ("M22-fallback-none", "else-branch returns None instead of 0", [
        (RET, '        return f\n    return None\n')]),
    ("M23-return-invert", "returns 2 - f", [
        (RET, '        return 2 - f\n    return 0\n')]),
    ("M24-key-default", "c.get('fullscreen', 0) default", [
        (KEY, '    f = c.get("fullscreen", 0)\n')]),
    ("M25-key-case", "reads 'Fullscreen' (absent key)", [
        (KEY, '    f = c.get("Fullscreen")\n')]),
    ("M26-key-floating-gate", "state read only for floating clients", [
        (KEY, '    f = c.get("fullscreen") if c.get("floating") is True else 0\n')]),
    # ---- verdict chain
    ("M27-branch-swap", "MAXIMIZED tested before FULLSCREEN", [
        (FS_BR + MAX_BR, MAX_BR + FS_BR)]),
    ("M28-max-truthiness", "MAXIMIZED tested as `elif fsmode:`", [
        (MAX_BR, '        elif fsmode:\n            verdict = "MAXIMIZED"\n')]),
    ("M29-fs-gt1", "FULLSCREEN tested as fsmode > 1", [
        (FS_BR, '        elif fsmode > 1:\n            verdict = "FULLSCREEN"\n')]),
    ("M30-max-ge1", "MAXIMIZED tested as fsmode >= 1", [
        (MAX_BR, '        elif fsmode >= 1:\n            verdict = "MAXIMIZED"\n')]),
    ("M31-max-and-floating", "MAXIMIZED requires floating (states only for floating)", [
        (MAX_BR, '        elif fsmode == 1 and floating:\n            verdict = "MAXIMIZED"\n')]),
    ("M32-fs-ne0", "FULLSCREEN tested as fsmode != 0", [
        (FS_BR, '        elif fsmode != 0:\n            verdict = "FULLSCREEN"\n')]),
    ("M33-badsize-only-flat", "BADSIZE only when fsmode == 0", [
        ('        if size is None:\n            verdict = "BADSIZE"\n',
         '        if size is None and fsmode == 0:\n            verdict = "BADSIZE"\n')]),
    ("M34-tiled-only-flat", "TILED only when fsmode == 0", [
        ('        elif not floating:\n',
         '        elif not floating and fsmode == 0:\n')]),
    ("M35-badsize-last", "BADSIZE tested after the two state branches", [
        (CHAIN,
         '        if fsmode == 2:\n'
         '            verdict = "FULLSCREEN"\n'
         '        elif fsmode == 1:\n'
         '            verdict = "MAXIMIZED"\n'
         '        elif size is None:\n'
         '            verdict = "BADSIZE"\n')]),
    # ---- tally / summary
    ("M36-max-counted-tiled", "MAXIMIZED counted in the tiled tally", [
        (TALLY, '        tally["tiled" if verdict == "MAXIMIZED" else verdict.lower()] += 1\n')]),
    ("M37-max-counted-fullscreen", "MAXIMIZED counted in the fullscreen tally", [
        (TALLY, '        tally["fullscreen" if verdict == "MAXIMIZED" else verdict.lower()] += 1\n')]),
    ("M38-fs-counted-maximized", "FULLSCREEN counted in the maximized tally", [
        (TALLY, '        tally["maximized" if verdict == "FULLSCREEN" else verdict.lower()] += 1\n')]),
    ("M39-states-values-swapped", "suffix values swapped, labels kept", [
        (STATES, '        states = " maximized=%d fullscreen=%d" % (t["fullscreen"], t["maximized"])\n')]),
    ("M40-states-no-space", "suffix leading space dropped", [
        (STATES, '        states = "maximized=%d fullscreen=%d" % (t["maximized"], t["fullscreen"])\n')]),
    ("M41-states-double-space", "suffix leading double space", [
        (STATES, '        states = "  maximized=%d fullscreen=%d" % (t["maximized"], t["fullscreen"])\n')]),
    ("M42-suffix-ge1", "suffix condition >= 1", [
        (SUFFIX, '    if t["maximized"] + t["fullscreen"] >= 1:\n')]),
    ("M43-suffix-gt-neg1", "suffix condition > -1", [
        (SUFFIX, '    if t["maximized"] + t["fullscreen"] > -1:\n')]),
    ("M44-states-after-verdict", "suffix printed after verdict=", [
        (FMT, '"matched=%d unmapped=%d agree=%d differ=%d tiled=%d badsize=%d verdict=%s%s" % ('),
        (ARGS, 't["tiled"], t["badsize"], verdict, states))')]),
    ("M45-states-before-tiled", "suffix printed before tiled=", [
        ("differ=%d tiled=%d badsize=%d%s verdict=%s", "differ=%d%s tiled=%d badsize=%d verdict=%s"),
        (ARGS, 'states, t["tiled"], t["badsize"], verdict))')]),
    # ---- counting reach
    ("M46-unmapped-fs-counted", "fullscreen counted for unmapped clients", [
        (UNMAPPED, UNMAPPED.replace(
            '            continue\n',
            '            tally["fullscreen"] += 1 if client_fsmode(c) == 2 else 0\n'
            '            continue\n'))]),
    ("M47-unmatched-fs-counted", "fullscreen counted for unmatched clients", [
        (NOMATCH, '        if want is None:\n'
                  '            tally["fullscreen"] += 1 if client_fsmode(c) == 2 else 0\n'
                  '            continue\n')]),
    ("M48-matched-unmatched", "unmatched clients counted as matched", [
        (NOMATCH, '        if want is None:\n            tally["matched"] += 1\n            continue\n')]),
    ("M49-differ-or-maximized", "maximized only dump exits 1 (DIFFER)", [
        ('    elif t["differ"] > 0:\n', '    elif t["differ"] > 0 or t["maximized"] > 0:\n')]),
    ("M50-top-verdict-maximized", "state clients change the top verdict word", [
        ('    else:\n        verdict, rc = "OK", 0\n',
         '    elif t["maximized"] + t["fullscreen"] > 0:\n'
         '        verdict, rc = "MAXIMIZED", 0\n'
         '    else:\n        verdict, rc = "OK", 0\n')]),
    ("M51-return-any-int", "membership test dropped, any JSON int returned raw", [
        ('    if isinstance(f, int) and not isinstance(f, bool) and f in (1, 2):\n'
         '        return f\n    return 0\n',
         '    if isinstance(f, int) and not isinstance(f, bool):\n'
         '        return f\n    return 0\n')]),
]


def main():
    ref = open(REF, encoding="utf-8").read()
    ref_lines = ref.count("\n")
    os.makedirs(SEAT, exist_ok=True)
    bad = 0
    print("mutant\tchanged_lines\tsha256\tnote")
    for name, note, pairs in SPEC:
        text = ref
        for old, new in pairs:
            n = text.count(old)
            if n != 1:
                print("BUILD %s replacement-count=%d for %r" % (name, n, old[:40]))
                bad += 1
                continue
            text = text.replace(old, new)
        if text == ref:
            print("BUILD %s unmutated" % name)
            bad += 1
            continue
        # count differing lines (difflib on lines)
        import difflib
        diff = [l for l in difflib.unified_diff(ref.splitlines(), text.splitlines(), lineterm="", n=0)
                if l[:1] in "+-" and l[:3] not in ("+++", "---")]
        p = os.path.join(SEAT, name + ".py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("%s\t%d\t%s\t%s" % (name, len(diff), hashlib.sha256(text.encode()).hexdigest()[:16], note))
    print("BUILD total=%d bad=%d ref_lines=%d" % (len(SPEC), bad, ref_lines))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
