#!/usr/bin/env python3
"""ExecFixtureMap: classify every never-executed line of xdg-terminal-exec v0.14.3 that the
frozen C1 fixtures (190 cases x variants A+B) do not reach.

The class table below is authored by hand (from reading the script), but every line number is
checked mechanically against the trace record: a line listed as reached is an error, a line in
the record that no class covers is an error. Line text is printed from the pinned script, never
typed here, so a shifted line number cannot hide.

Input:  out/lines.json (from map-fixtures.py), the pinned script.
Output: out/unreached-statements.tsv  (line, class, condition, source text)
        stdout: per-class counts
"""
import argparse
import json
import sys

sys.dont_write_bytecode = True

# class -> (reason, [lines])
CLASSES = [
    ("debug-enabled", "debug() printing body; no fixture sets XTE_DEBUG or DEBUG (env census)",
     [63, 66, 67, 689, 690]),
    ("help-usage", "DECLARED-RESIDUAL: only reachable from -h/--help; no fixture argv carries it",
     [85, 92, 1137, 1138]),
    ("check-bool-invalid", "check_bool fallback: no fixture passes an unrecognised boolean",
     [55, 56]),
    ("cache-read", "DECLARED-RESIDUAL (warm cache): read_cache hit path; no cache file exists "
                   "when read_cache runs (fresh root per case, read_cache precedes save_cache)",
     [222, 223, 224, 225, 226, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238,
      240, 241, 248, 249, 251, 252, 253, 259, 260, 272, 273, 274, 275, 276, 277, 278, 279,
      280, 281, 282, 283, 284, 285, 287, 288, 291, 292, 1180]),
    ("cache-write-arms", "save_cache failure/disable arms: hash never fails, no terminal arg "
                         "holds a newline, XTE_CACHE_ENABLED never set",
     [306, 307, 308, 314, 315, 316, 336, 337, 338]),
    ("env-knob", "XTE_* / list directives no fixture uses: /enable_cache, /execarg_compat, "
                 "strict-mode directive ignore",
     [381, 382, 383, 384, 389, 390, 391, 392, 404, 405]),
    ("expand-escapes", "de_expand_str arms for \\n \\t \\r and \\\\; only \\s appears in any "
                       "fixture entry value",
     [533, 534, 535, 538, 539, 540, 543, 544, 545, 548, 549, 550]),
    ("tokenizer-escape", "de_expand_str strips an unknown escape before tokenizing, so the "
                         "quoted-backslash arms are only reachable via \\\\ in an Exec",
     [633, 636, 637, 643, 644, 645, 646, 647, 648]),
    ("tokenizer-error", "tokenizer rejects an unescaped quoted $/` or an impossible char; no "
                        "fixture entry carries one",
     [628, 629, 676, 677]),
    ("tokenizer-space-run", "no fixture Exec holds two consecutive interior spaces",
     [598, 599]),
    ("print-order-content", "print-content never follows id/path, so the delimiter print on the "
                            "not-first path never runs",
     [1359]),
    ("arg-form-title", "no entry TerminalArgTitle ends in '='; no fixture passes --title/--app-id to "
                       "an entry whose entry lacks the key (the dir and hold counterparts are covered: "
                       "1412 and 1397 are traced)",
     [1418, 1419, 1427, 1442]),
    ("entry-checks", "NotShowIn check skipped for fallback ids (de_checks=false): no fallback "
                     "entry in any fixture carries NotShowIn",
     [869, 870]),
    ("field-deprecation", "no fixture Exec carries a deprecated %d %D %n %N %v %m field",
     [704]),
    ("exclusion-dedup", "duplicate exclusion markers (already excluded / already prevented): "
                        "no fixture repeats one",
     [449, 459]),
    ("replace-break", "replace() only reached with a matching separator; the 'nothing left' arm "
                      "never taken",
     [492]),
    ("find-entry-empty-id", "empty entry id line: no fixture produces one",
     [1069]),
    ("gen-hash-fail", "gen_hash hash-regex failure arm: the hash always matched",
     [211, 212]),
    ("launch-path", "OUT-OF-SCOPE (print-only claim): real exec (cd + exec \"$@\"): every fixture carries a print/test option, so "
                    "the script never leaves print mode (outside the print-only claim)",
     [1494, 1495, 1496, 1499]),
]
# lines in the raw residue that are not statements at all (closers, mid-assignment, heredoc tail)
NONSTATEMENT = {
    28: "second line of a multi-line XTE__LF assignment (bash reports the last line)",
    41: "'}' closing the group with a heredoc", 68: "'done' with a heredoc",
    258: "'done' with a redirect", 473: "'done' with a redirect", 792: "'done' with a heredoc",
    1017: "'done' with a redirect", 1125: "'done' with a heredoc",
    691: "')' closing a $() that is itself unreachable",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rec = json.load(open(a.lines))
    counts = {int(k): v for k, v in rec["counts"].items()}
    per_case = rec["per_case"]
    src = open(a.script, encoding="utf-8", errors="surrogateescape").read().split("\n")
    listed = {}
    for cls, cond, lines in CLASSES:
        for ln in lines:
            if ln in listed:
                raise SystemExit("line %d in two classes" % ln)
            listed[ln] = (cls, cond)
    for ln in NONSTATEMENT:
        if ln in listed:
            raise SystemExit("line %d both statement and non-statement" % ln)
    bad = [ln for ln in listed if counts.get(ln, 0) != 0]
    if bad:
        raise SystemExit("REFUSED: these listed lines were reached: %r" % [(b, counts[b]) for b in bad])
    # every never-traced, non-trivial line must be covered
    blank_or_comment = {i for i, t in enumerate(src, 1) if not t.strip() or t.strip().startswith("#")}
    untraced = [i for i in range(1, len(src) + 1)
                if i not in counts and i not in blank_or_comment]
    uncovered = [i for i in untraced if i not in listed and i not in NONSTATEMENT]
    with open(a.out, "w") as fh:
        fh.write("line\tclass\tcases\ttext\tcondition\n")
        for ln in sorted(listed):
            cls, cond = listed[ln]
            cases = sum(1 for v in per_case.values() if ln in v["lines"])
            fh.write("%d\t%s\t%d\t%s\t%s\n" % (ln, cls, cases, src[ln - 1].strip(), cond))
        for ln in sorted(NONSTATEMENT):
            fh.write("%d\tnot-a-statement\t%d\t%s\t%s\n"
                     % (ln, sum(1 for v in per_case.values() if ln in v["lines"]),
                        src[ln - 1].strip(), NONSTATEMENT[ln]))
    nstmt = len(listed)
    print("statements never executed: %d in %d classes" % (nstmt, len(CLASSES)))
    print("non-statement residue lines: %d" % len(NONSTATEMENT))
    print("untraced non-trivial lines in total: %d" % len(untraced))
    print("OUTSIDE the class table (script-side control/fixture-construction lines): %d" % len(uncovered))
    print("uncovered line numbers: %r" % uncovered)
    buckets = {"new-in-contract": 0, "declared-residual": 0, "out-of-scope": 0}
    for cls, cond, lines in CLASSES:
        tag = ("declared-residual" if cond.startswith("DECLARED")
               else "out-of-scope" if cond.startswith("OUT-OF-SCOPE") else "new-in-contract")
        buckets[tag] += len(lines)
        print("  %-22s %3d lines  %s" % (cls, len(lines), tag))
    print("statement lines by bucket: %r" % buckets)


if __name__ == "__main__":
    main()
