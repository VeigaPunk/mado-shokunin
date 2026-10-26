#!/usr/bin/env python3
"""check-locators.py - recompute prose source locators against pinned receipts.

Read-only checker for the mado lane's prose (markdown, LOG.md). It finds every
locator token ``<name>:<N>[-<M>][,<N2>[-<M2>]...]`` whose basename is a file in
``--fetch DIR`` (a directory of pinned receipts), takes the backticked code
fragments of the same prose line, and decides whether the cited receipt lines
actually carry the identifiers of the fragment the locator is attached to.

Rules (deliberately simple; the seat report names the limits):

* Name resolution: the token's basename - after stripping every path component,
  so a ``fetch/`` or ``dir/`` prefix does no harm - must equal a file name in
  ``--fetch DIR``. Tokens whose name does not resolve are not checked and are
  not printed (``--explain`` prints them as ``SKIP``).
* Ranges: ``N`` is the single 1-based line N; ``N-M`` is inclusive; a reversed
  range ``M-N`` with M > N is normalised to ``N-M``; several ranges are OR-ed.
* Fragments: every backticked span on the prose line that is not itself a
  resolved locator and that contains at least one identifier token
  (``[A-Za-z_][A-Za-z0-9_]*``, length >= 3). ``fragments=<k>`` counts them;
  ``supported=<j>`` counts those whose every identifier token occurs, at an
  identifier boundary, in the union of the cited receipt lines.
* Attribution: a locator cites the nearest fragment *before* it on the line,
  else the nearest *after* it. The verdict is decided by that fragment alone:
  ``OK`` supported, ``MISS`` not supported, ``NOFRAG`` no fragment on the line.
  ``supported=<j>`` still reports every same-line fragment, so a line can print
  ``supported=1 verdict=MISS`` when the one supported fragment is a different
  fact than the one the locator belongs to.
* Identifier tokens are a proxy for the fact, not the fact. Prose without
  backticks is visible only as ``NOFRAG``: the locator is in range but nothing
  is checked. A locator citing a receipt line that happens to carry the same
  identifiers for a different statement is supported falsely.

Output: one line per locator
``LOC <prose-file>:<line> <locator> fragments=<k> supported=<j> verdict=OK|MISS|NOFRAG``
and a final ``CHECK_LOCATORS: locators=<n> miss=<m>``.
Exit: 0 no miss, 1 some miss, 2 usage error.

``--selftest`` builds its fixtures in a private temporary directory, runs the
same code path over them, and re-runs the case table with the range-inclusion
comparison flipped; it fails unless every case matches and the flipped
comparison breaks the table (teeth).
"""

import argparse
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile

ID_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
LOCATOR_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"(?P<name>[A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z0-9_]+)"
    r":(?P<ranges>[0-9]+(?:-[0-9]+)?(?:,[0-9]+(?:-[0-9]+)?)*)"
    r"(?![0-9A-Za-z_])"
)
FRAG_RE = re.compile(r"`([^`\n]+)`")


class UsageError(Exception):
    pass


def parse_ranges(spec):
    """`394-395,412-413` -> [(394, 395), (412, 413)]; reversed ranges normalised."""
    ranges = []
    for part in spec.split(","):
        if "-" in part:
            lo_s, hi_s = part.split("-", 1)
            lo, hi = int(lo_s), int(hi_s)
            if hi < lo:
                lo, hi = hi, lo
            ranges.append((lo, hi))
        else:
            n = int(part)
            ranges.append((n, n))
    return ranges


def in_ranges(n, ranges):
    """Inclusive range test. The selftest flips this comparison to prove teeth."""
    return any(lo <= n <= hi for lo, hi in ranges)


def load_receipt(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def cited_text(lines, ranges):
    """Union of the cited receipt lines, file order; line numbers outside the file are absent.

    ``in_ranges`` is the only range test, so the selftest's flipped comparison reaches every verdict.
    """
    return "\n".join(lines[i - 1] for i in range(1, len(lines) + 1) if in_ranges(i, ranges))


def token_occurs(tok, text):
    return re.search(r"(?<![A-Za-z0-9_])" + re.escape(tok) + r"(?![A-Za-z0-9_])", text) is not None


def fragment_tokens(frag):
    toks = set(ID_RE.findall(frag))
    return sorted(t for t in toks if len(t) >= 3)


def resolve_name(name, fetch_names):
    """Basename of the locator name, if it is a file in the fetch dir, else None."""
    base = name.rsplit("/", 1)[-1]
    return base if base in fetch_names else None


def _candidates(line, fetch_names):
    """Backticked same-line fragments that are not themselves resolved locators."""
    cands = []
    for m in FRAG_RE.finditer(line):
        text = m.group(1)
        loc = LOCATOR_RE.fullmatch(text.strip())
        if loc is not None and resolve_name(loc.group("name"), fetch_names) is not None:
            continue
        toks = fragment_tokens(text)
        if not toks:
            continue
        cands.append((m.start(), m.end(), text, toks))
    return cands


def check_line(prose_path, lineno, line, fetch_names, receipts, fetch_dir, explain):
    """Return (output lines, locators seen, misses) for one prose line."""
    out = []
    cands = _candidates(line, fetch_names)
    locators = []
    for m in LOCATOR_RE.finditer(line):
        base = resolve_name(m.group("name"), fetch_names)
        if base is None:
            if explain:
                out.append("SKIP %s:%d %s reason=unresolved-name" % (prose_path, lineno, m.group(0)))
            continue
        locators.append((m.start(), m.end(), m.group(0), base, parse_ranges(m.group("ranges"))))

    seen = 0
    miss = 0
    for ls, le, token, base, ranges in locators:
        if base not in receipts:
            receipts[base] = load_receipt(os.path.join(fetch_dir, base))
        text = cited_text(receipts[base], ranges)
        support = {c[2]: all(token_occurs(t, text) for t in c[3]) for c in cands}
        before = [c for c in cands if c[1] <= ls]
        after = [c for c in cands if c[0] >= le]
        attr = before[-1] if before else (after[0] if after else None)
        if attr is None:
            verdict = "NOFRAG"
        elif support[attr[2]]:
            verdict = "OK"
        else:
            verdict = "MISS"
        seen += 1
        if verdict == "MISS":
            miss += 1
        out.append(
            "LOC %s:%d %s fragments=%d supported=%d verdict=%s"
            % (prose_path, lineno, token, len(cands), sum(1 for c in cands if support[c[2]]), verdict)
        )
        if explain:
            out.append("  ATTR %s" % ("-" if attr is None else repr(attr[2])))
            for c in cands:
                out.append(
                    "  FRAG %s tokens=%s supported=%s"
                    % (repr(c[2]), ",".join(c[3]), "yes" if support[c[2]] else "no")
                )
    return out, seen, miss


def run(fetch_dir, prose_paths, explain=False):
    """Check every prose file; return (output lines, locator count, miss count)."""
    if not os.path.isdir(fetch_dir):
        raise UsageError("--fetch %s is not a directory" % fetch_dir)
    fetch_names = {n for n in os.listdir(fetch_dir) if os.path.isfile(os.path.join(fetch_dir, n))}
    receipts = {}
    out = []
    total = 0
    misses = 0
    for prose_path in prose_paths:
        if not os.path.isfile(prose_path):
            raise UsageError("prose file %s does not exist" % prose_path)
        try:
            with open(prose_path, "r", encoding="utf-8", errors="replace") as fh:
                prose_lines = fh.read().splitlines()
        except OSError as exc:
            raise UsageError("cannot read prose file %s: %s" % (prose_path, exc))
        for lineno, line in enumerate(prose_lines, 1):
            lines, seen, miss = check_line(
                prose_path, lineno, line, fetch_names, receipts, fetch_dir, explain
            )
            out.extend(lines)
            total += seen
            misses += miss
    return out, total, misses


# ---------------------------------------------------------------- selftest

REC = [
    "// fixture receipt for check-locators selftest",
    "    int alpha = 1;",
    "    int beta = 2;",
    "    // gamma is a comment",
    "    return alpha + beta;",
    "}",
    "",
    "    delta_line = 8;",
    "    int epsilon = 9;",
]
PLAIN = [
    "# plain fixture",
    "plainvalue=1",
    "other=2",
]

# (prose line, expected LOC lines for that line as (fragments, supported, verdict))
CASES = [
    ("`alpha` at `rec.cpp:2`", [(1, 1, "OK")]),
    ("`beta` at `rec.cpp:2`", [(1, 0, "MISS")]),
    ("`alpha` at `rec.cpp:900`", [(1, 0, "MISS")]),
    ("see `rec.cpp:4` alone", [(0, 0, "NOFRAG")]),
    ("`alpha` `beta` at `rec.cpp:2-5`", [(2, 2, "OK")]),
    ("`alpha` at `rec.cpp:9,2`", [(1, 1, "OK")]),
    ("`gamma` at `rec.cpp:4-3`", [(1, 1, "OK")]),
    ("`alpha` at `rec.cpp:2` and `beta` at `rec.cpp:3`", [(2, 1, "OK"), (2, 1, "OK")]),
    ("`alpha` at `rec.cpp:3` and `beta` at `rec.cpp:2`", [(2, 1, "MISS"), (2, 1, "MISS")]),
    ("`plainvalue` at `plain.conf:2`", [(1, 1, "OK")]),
    ("`ab` at `plain.conf:2`", [(0, 0, "NOFRAG")]),
    ("`alpha` at otherfile.cpp:2", []),
    ("`alpha` at `fetch/rec.cpp:5`", [(1, 1, "OK")]),
    ("`alpha` at `sub/dir/rec.cpp:5`", [(1, 1, "OK")]),
    ("`return` at `rec.cpp:5`", [(1, 1, "OK")]),
    ("`alpha beta` at `rec.cpp:2`", [(1, 0, "MISS")]),
    ("nothing backticked here rec.cpp:2", [(0, 0, "NOFRAG")]),
    ("`ALPHA` at `rec.cpp:2`", [(1, 0, "MISS")]),
]


def _build_fixtures(root):
    probe = os.path.join(root, "fetch")
    os.makedirs(probe)
    with open(os.path.join(probe, "rec.cpp"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(REC) + "\n")
    with open(os.path.join(probe, "plain.conf"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(PLAIN) + "\n")
    prose = os.path.join(root, "prose.md")
    with open(prose, "w", encoding="utf-8") as fh:
        fh.write("\n".join(c[0] for c in CASES) + "\n")
    return probe, prose


def _verdicts(out_lines, prose_path, lineno):
    got = []
    prefix = "LOC %s:%d " % (prose_path, lineno)
    for line in out_lines:
        if not line.startswith(prefix):
            continue
        m = re.search(r"fragments=(\d+) supported=(\d+) verdict=(OK|MISS|NOFRAG)$", line)
        got.append((int(m.group(1)), int(m.group(2)), m.group(3)))
    return got


def _run_cases(probe, prose):
    out, total, misses = run(probe, [prose])
    return out, total, misses


def selftest():
    root = tempfile.mkdtemp(prefix="check-locators-selftest.")
    try:
        probe, prose = _build_fixtures(root)
        out, total, misses = _run_cases(probe, prose)
        k = len(CASES)
        ok = 0
        failures = []
        for lineno, (text, expected) in enumerate(CASES, 1):
            got = _verdicts(out, prose, lineno)
            if got == expected:
                ok += 1
            else:
                failures.append("case %d %r: expected %r got %r" % (lineno, text, expected, got))
        expected_total = sum(len(c[1]) for c in CASES)
        expected_miss = sum(1 for c in CASES for v in c[1] if v[2] == "MISS")
        if total != expected_total:
            failures.append("locator count expected %d got %d" % (expected_total, total))
            ok -= 1
        if misses != expected_miss:
            failures.append("miss count expected %d got %d" % (expected_miss, misses))
            ok -= 1
        print("SELFTEST: cases=%d passed=%d locators=%d miss=%d" % (k, ok, total, misses))

        # teeth: flip the range-inclusion comparison and require the table to break,
        # in both directions (an OK must become MISS, a MISS must become OK).
        global in_ranges
        real = in_ranges
        try:
            in_ranges = lambda n, ranges: not any(lo <= n <= hi for lo, hi in ranges)
            flipped_out, flipped_total, _ = _run_cases(probe, prose)
        finally:
            in_ranges = real
        flips = 0
        ok_to_miss = 0
        miss_to_ok = 0
        for lineno, (text, expected) in enumerate(CASES, 1):
            got = _verdicts(flipped_out, prose, lineno)
            for exp, flip in zip(expected, got):
                if exp == flip:
                    continue
                flips += 1
                if exp[2] == "OK" and flip[2] == "MISS":
                    ok_to_miss += 1
                elif exp[2] == "MISS" and flip[2] == "OK":
                    miss_to_ok += 1
        print(
            "SELFTEST: teeth flipped_table_broken=%s flips=%d ok_to_miss=%d miss_to_ok=%d"
            % (
                "yes" if (flips and ok_to_miss and miss_to_ok) else "no",
                flips,
                ok_to_miss,
                miss_to_ok,
            )
        )
        if flips == 0 or ok_to_miss == 0 or miss_to_ok == 0:
            failures.append(
                "teeth: flipping in_ranges must break the table both ways "
                "(flips=%d ok_to_miss=%d miss_to_ok=%d)" % (flips, ok_to_miss, miss_to_ok)
            )

        # exit codes: a run with misses exits 1, usage errors exit 2.
        sink = io.StringIO()
        errsink = io.StringIO()
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(errsink):
            rc_miss = main(["--fetch", probe, prose])
            rc_noarg = main([])
            rc_selftest_with_args = main(["--selftest", "--fetch", probe])
            rc_missing_dir = main(["--fetch", os.path.join(root, "nope"), prose])
        if rc_miss != 1:
            failures.append("exit code with misses expected 1 got %d" % rc_miss)
        for label, rc in (
            ("no arguments", rc_noarg),
            ("--selftest with other arguments", rc_selftest_with_args),
            ("missing fetch dir", rc_missing_dir),
        ):
            if rc != 2:
                failures.append("exit code for %s expected 2 got %d" % (label, rc))

        if failures:
            for f in failures:
                print("SELFTEST: FAIL %s" % f)
            print("SELFTEST: FAIL")
            return 1
        if k != ok or k < 12:
            print("SELFTEST: FAIL cases=%d passed=%d (need k==n and k>=12)" % (k, ok))
            return 1
        print("SELFTEST: PASS")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


# -------------------------------------------------------------------- main


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="recompute prose source locators against pinned receipts (read-only)"
    )
    ap.add_argument("--fetch", metavar="DIR", help="directory of pinned receipts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture table and the teeth check")
    ap.add_argument("--explain", action="store_true", help="also print SKIP/ATTR/FRAG detail lines")
    ap.add_argument("prose", nargs="*", help="markdown prose files to check")
    args = ap.parse_args(argv)

    if args.selftest:
        if args.prose or args.fetch or args.explain:
            print("usage: --selftest takes no other arguments", file=sys.stderr)
            return 2
        return selftest()

    try:
        if not args.fetch:
            raise UsageError("--fetch DIR is required")
        if not args.prose:
            raise UsageError("at least one prose file is required")
        out, total, misses = run(args.fetch, args.prose, explain=args.explain)
    except UsageError as exc:
        print("usage error: %s" % exc, file=sys.stderr)
        return 2

    for line in out:
        print(line)
    print("CHECK_LOCATORS: locators=%d miss=%d" % (total, misses))
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main())
