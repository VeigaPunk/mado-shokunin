#!/usr/bin/env python3
"""check-round-outcome-first.py — check for QUALITY criterion 99 (round-48; drafted by seat ScrConsider as "check96", renumbered at landing).

Question answered: does a round's closure section in ``SCORECARD.md`` lead with the round-level outcome — what the host's
desktop tooling can now do, named by the path that carries it — or does it lead with the round's own bookkeeping
(registration freeze, counter ids, seat/wave counts)?

Ground: ``considerthese/2026-10-26.md`` proposal 6 (2026-10-26), "Lead with round-level outcomes, not counter internals".

== RULE (stated before the first run) ==

Input: a git repository and a revision; ``SCORECARD.md`` is read from the object database (``git show <rev>:SCORECARD.md``),
the working tree is never touched.

Section: the lines from ``^## Round <N>`` up to the next line starting ``## ``.

First paragraph: the run of non-blank section lines that follows the heading, ending at the first blank line, at the first
table row (a line starting ``|``), or at the next heading. Its line number is reported.

First sentence: the first paragraph's text joined with single spaces, cut at the first ``.``/``!``/``?`` that is followed by
whitespace or the end of the text (a period inside a path such as ``tools/mado-terminal.py`` or a version such as
``v0.14.3`` is not followed by whitespace and does not cut).

Desktop-facing surface, from criterion 60's definition: ``tools/mado-<name>.py``, ``tools/mado-<name>.sh``,
``corpus/knowledge/<name>.md``, ``SKILL.md``, ``PROVINCE.md``.

Process token (frozen list, matched case-insensitively except where a case is written): ``Registration`` (any case),
``frozen``, ``freeze``, ``Claims declared``, ``PRED-``, ``TARGET_MET``, ``TARGET_MISSED``, ``fixtures=``, ``seats?``,
``wave``, ``attempt=``, ``receipts/``, ``counter``.

``PASS`` iff the first sentence names a desktop-facing surface **and** carries no process token. Anything else is
``FAIL`` with the reason named: ``no-surface`` (the surface is absent from the first sentence), ``process-first`` (a
process token sits in the first sentence), ``no-paragraph`` (the section is missing or has no prose before its table).

Output, one line per round, then the summary line exactly::

    OUTCOME_FIRST: round=<N> verdict=PASS|FAIL line=<n> surface=<path|none> process_tokens=<k> reasons=<none|...>

Exit status: 0 all rounds PASS, 1 any FAIL, 2 usage or git error.

Usage::

    check-round-outcome-first.py --repo <dir> --rev <rev> --round <N> [--round <N> ...]
    check-round-outcome-first.py --repo <dir> --rev <rev> --rounds <a>-<b> [--rounds <c>-<d> ...]
    check-round-outcome-first.py --rule
    check-round-outcome-first.py --selftest [--verbose]

``--selftest`` builds a throwaway git repository under ``$TMPDIR`` (never ``/tmp`` by preference; ``tempfile`` honours
``TMPDIR``) with four synthetic round sections — a positive control that leads with the outcome, a process-first negative,
a negative whose surface appears only in the second sentence, and a negative with no prose at all — and scores them.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

SURFACE = re.compile(
    r"(tools/mado-[a-z0-9-]+\.(?:py|sh)|corpus/knowledge/[a-z0-9-]+\.md|SKILL\.md|PROVINCE\.md)"
)
PROCESS = re.compile(
    r"(registration|frozen|freeze|claims declared|PRED-|TARGET_MET|TARGET_MISSED|fixtures=|seats?|wave|attempt=|receipts/|counter)",
    re.IGNORECASE,
)
ROUND_HEAD = re.compile(r"^## Round (\d+)")


def read_scorecard(repo, rev):
    p = subprocess.run(
        ["git", "-C", repo, "show", "%s:SCORECARD.md" % rev],
        capture_output=True, text=True,
    )
    if p.returncode != 0:
        raise SystemExit("git show %s:SCORECARD.md failed: %s" % (rev, p.stderr.strip()[:200]))
    return p.stdout.split("\n")


def section(lines, number):
    """Return [(lineno, text)] of the round's section, 1-based line numbers."""
    start = None
    for i, line in enumerate(lines, 1):
        m = ROUND_HEAD.match(line)
        if m and int(m.group(1)) == number:
            start = i
            break
    if start is None:
        return None
    out = []
    for i in range(start, len(lines)):
        line = lines[i]
        if i > start - 1 and line.startswith("## "):
            break
        out.append((i + 1, line))
    return out


def first_paragraph(body):
    """body excludes the heading; returns (lineno, text) or (0, '')."""
    acc, first_line = [], 0
    for lineno, line in body:
        if not line.strip():
            if acc:
                break
            continue
        if line.startswith("|") or line.startswith("#"):
            if acc:
                break
            continue
        if not acc:
            first_line = lineno
        acc.append(line.strip())
    return first_line, " ".join(acc)


def first_sentence(text):
    for i, ch in enumerate(text):
        if ch in ".!?" and (i + 1 == len(text) or text[i + 1].isspace()):
            return text[: i + 1]
    return text


def exists_at(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return p.returncode == 0


def score(lines, number, repo=None, rev=None):
    body = section(lines, number)
    if body is None:
        return dict(round=number, verdict="SKIP", line=0, surface="none", tokens=0, reasons=["no-section"])
    lineno, para = first_paragraph([(n, l) for n, l in body if not ROUND_HEAD.match(l)])
    if not para:
        return dict(round=number, verdict="FAIL", line=lineno, surface="none", tokens=0, reasons=["no-paragraph"])
    sent = first_sentence(para)
    m = SURFACE.search(sent)
    tokens = PROCESS.findall(sent)
    reasons = []
    if not m:
        reasons.append("no-surface")
    elif repo and rev and not exists_at(repo, rev, m.group(1)):
        reasons.append("surface-absent")
    if tokens:
        reasons.append("process-first")
    return dict(
        round=number, verdict="FAIL" if reasons else "PASS", line=lineno,
        surface=m.group(1) if m else "none", tokens=len(tokens), reasons=reasons or ["none"],
    )


def emit(results):
    failed = sum(1 for r in results if r["verdict"] == "FAIL")
    skipped = sum(1 for r in results if r["verdict"] == "SKIP")
    for r in results:
        print("OUTCOME_FIRST: round=%d verdict=%s line=%d surface=%s process_tokens=%d reasons=%s"
              % (r["round"], r["verdict"], r["line"], r["surface"], r["tokens"], ",".join(r["reasons"])))
    print("OUTCOME_FIRST_SUMMARY: rounds=%d pass=%d fail=%d skip=%d"
          % (len(results), len(results) - failed - skipped, failed, skipped))
    return 1 if failed else 0


FIXTURE = """# SCORECARD fixture (check96 selftest)

## Round 1 - positive control

SUPER+RETURN now predicts the resolver's warm-cache answer from `tools/mado-terminal.py`, so the hotkey's command is
readable before the key is pressed. Registration and freeze bookkeeping follow below.

| Claim | Verdict |
|---|---|
| C1 | TARGET_MET |

## Round 2 - process-first negative

Registration `.ufo/waves/round-2/registration.md`, frozen at `deadbeef` after wave `w1`. The round moved
`tools/mado-terminal.py`.

| Claim | Verdict |
|---|---|
| C1 | TARGET_MET |

## Round 3 - surface only in the second sentence

The round closed on attempt 1 with 12 seats. It moved `corpus/knowledge/xdg-terminal-selection-r47.md`.

| Claim | Verdict |
|---|---|
| C2 | TARGET_MET |

## Round 4 - no prose

| Claim | Verdict |
|---|---|
| C1 | TARGET_MET |

## Round 5 - outcome-first sentence naming a path that is not in the tree

`tools/mado-ghost.py` now answers the round's question.

| Claim | Verdict |
|---|---|
| C1 | TARGET_MET |
"""


def selftest(verbose):
    d = tempfile.mkdtemp(prefix="check96-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), "selftest repo is not the fixture dir: %s" % top
        for rel in ("tools/mado-terminal.py", "corpus/knowledge/xdg-terminal-selection-r47.md"):
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            open(os.path.join(d, rel), "w").write("fixture\n")
        with open(os.path.join(d, "SCORECARD.md"), "w") as fh:
            fh.write(FIXTURE)
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@invalid",
                        "commit", "-q", "-m", "fixture"], check=True)
        rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True,
                             check=True).stdout.strip()
        lines = read_scorecard(d, rev)
        got = {n: score(lines, n, d, rev) for n in (1, 2, 3, 4, 5)}
        want = {1: "PASS", 2: "FAIL", 3: "FAIL", 4: "FAIL", 5: "FAIL"}
        ok = all(got[n]["verdict"] == want[n] for n in want)
        if got[2]["verdict"] == "FAIL" and "process-first" not in got[2]["reasons"]:
            ok = False
        if got[3]["verdict"] == "FAIL" and "no-surface" not in got[3]["reasons"]:
            ok = False
        if got[4]["reasons"] != ["no-paragraph"]:
            ok = False
        if got[5]["reasons"] != ["surface-absent"]:
            ok = False
        if verbose or not ok:
            for n in sorted(got):
                r = got[n]
                print("selftest round=%d want=%s got=%s line=%d surface=%s reasons=%s"
                      % (n, want[n], r["verdict"], r["line"], r["surface"], ",".join(r["reasons"])))
        print("SELFTEST: %s cases=5" % ("ok" if ok else "fail"))
        return 0 if ok else 1
    finally:
        for root, dirs, files in os.walk(d, topdown=False):
            for name in files:
                os.unlink(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(d)


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--round", type=int, action="append", default=[])
    ap.add_argument("--rounds", action="append", default=[])
    ap.add_argument("--rule", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest(args.verbose)
    if args.rule:
        print(__doc__.split("== RULE (stated before the first run) ==")[1].split("Output, one line")[0].strip())
        return 0
    if not (args.repo and args.rev):
        print(__doc__.split("Usage::")[1].strip(), file=sys.stderr)
        return 2
    numbers = list(args.round)
    for spec in args.rounds:
        m = re.match(r"^(\d+)-(\d+)$", spec)
        if not m:
            print("bad --rounds %r" % spec, file=sys.stderr)
            return 2
        a, b = int(m.group(1)), int(m.group(2))
        if a > b:
            print("bad --rounds %r (descending)" % spec, file=sys.stderr)
            return 2
        numbers.extend(range(a, b + 1))
    if not numbers:
        print("no --round/--rounds given", file=sys.stderr)
        return 2
    lines = read_scorecard(args.repo, args.rev)
    return emit([score(lines, n, args.repo, args.rev) for n in numbers])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
