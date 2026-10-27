#!/usr/bin/env python3
"""c1-r52-ledger.py — PRED-C1-r52 (draft): the tracked tool ledger is accountable.

Seat C1CounterDesign, mado round 52, w1.  DRAFT — not the scored artifact; the
integration path is `quality/counters/c1-r52-ledger.py`.

The frozen predicate this draft answers (registration.md, round 52, C1):

  a new counter for the tracked instrument ledger runs at a requested pinned revision,
  and validates population row uniqueness, resolvable evidence pointer, non-self
  pointer, and a description containing instrument-specific functional context.  It
  must pass on the existing production ledger at the base revision and fail on
  `controls/c1-do-nothing.md` specifically for self-pointer/context defects.

What it measures (every byte from `--rev`; the working tree is never read)

  p  population   one `git ls-tree -r --name-only <rev>` listing: every file under
                  `tools/` (any extension, `__pycache__`/`.pyc`/`.pyo` excluded) plus
                  the direct children `quality/*.py` and `quality/counters/*.py`.
                  This is the predicate's P; the ledger never defines the population.
  r  ledger_rows  parsed pipe-table rows of `quality/tool-ledger.md` at `<rev>`
                  (fenced blocks are documentation, never rows).  A row is any pipe row
                  whose first cell names a path; cells are path | description | pointer
                  region.  Rows with MORE than three cells are tolerated: the frozen
                  do-nothing control is a four-cell table, and the claim requires that
                  control to fail for self-pointer/context reasons — a counter that
                  throws such a row away as malformed can never see those reasons.
  u  uncovered    population paths with no row.
  d  dup          repeated row path (population row uniqueness).
  g  dangling     row path that is not a population path.
                  (A row wider than the ledger's three-cell grammar is scored, not
                  discarded: the frozen do-nothing control is a four-cell table, and a
                  counter that threw such a row away could never name its defect.)
  b  bad_pointer  the accountability pointer is not an accountable document: either no
                  target in the pointer region (cells 3..) resolves at `<rev>` to an
                  existing file whose bytes name the row file's basename as a name, or
                  the only such target is a *peer instrument* — a sibling tool's own
                  source file, which may name this basename in passing but is not
                  accountable for it.  The pointer region is the ledger's own grammar
                  (cell 3), so a path mentioned only in prose elsewhere in the row
                  cannot substitute for the accountable pointer.
  s  self_pointer a cell of the row names the ledger under test (`quality/tool-ledger.md`)
                  or the row's own path.  Such a pointer resolves — the ledger's bytes
                  contain every instrument basename — and is accountable for nothing:
                  it is the round-51 hole this claim names.
  c  generic_desc the description carries no instrument-specific functional context:
                  empty/placeholder, shared verbatim with another row, too short,
                  sharing no two-word phrase with the instrument's own bytes at `<rev>`,
                  or bound only by a phrase made of the instrument's own path words
                  ("c2 r51"), which restates the name rather than the function.  The
                  binding is lexical, not entailment — see the report's ceiling note.

The summary line is the last line and always carries the same fields:

  C1_R52: population=<P> ledger_rows=<R> uncovered=<n> dup=<n> dangling=<n> \
bad_pointer=<n> self_pointer=<n> generic_desc=<n> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit codes: 0 = TARGET_MET, 1 = TARGET_MISSED (absent ledger or any defect), 2 =
setup error (bad --repo/--rev/--work).

Usage:
  python3 -I c1-r52-ledger.py --repo <lane> --rev <rev> [--ledger <file>]
  python3 -I c1-r52-ledger.py --selftest --work <scratch>
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

LEDGER_REL = "quality/tool-ledger.md"
SELFTEST_CHECKS = 53
REFUSED_WORK_PREFIXES = ("/tmp", "/var/tmp", "/dev/shm")

# The ledger's own row grammar.
EMPHASIS = "`*_ \t"
SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")
LINE_SUFFIX = re.compile(r":\d+(?:-\d+)?$")
BACKTICK = re.compile(r"`([^`\n]+)`")
POINTER_TOKEN = re.compile(r"^`([^`]+)`$")
PLACEHOLDER = re.compile(r"^[\s\-–—_*`.?]+$")
NAME_BOUND = r"(?<![A-Za-z0-9._-])%s(?![A-Za-z0-9_-])"

# A description must have at least this many words to be a description at all.
MIN_DESC_WORDS = 5
# The summary line carries the exact count; the detail list is capped so a coverage
# failure does not bury the defect signals that matter.
MAX_UNCOVERED_DETAILS = 8
WORD = re.compile(r"[a-z0-9]+")


class SetupError(Exception):
    """The question cannot be answered (exit 2)."""


# --------------------------------------------------------------------------
# read-only git
# --------------------------------------------------------------------------

def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.setdefault("LC_ALL", "C.UTF-8")
    return env


def git(repo, *args):
    proc = subprocess.run(("git", "-C", repo) + args, capture_output=True, env=git_env())
    if proc.returncode != 0:
        raise SetupError("git %s failed in %s: %s" % (
            " ".join(args), repo, proc.stderr.decode("utf-8", "replace").strip()[:300]))
    return proc.stdout


def resolve_rev(repo, rev):
    try:
        out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}").decode(
            "utf-8", "replace").strip()
    except SetupError:
        raise SetupError("--rev %r does not resolve to a commit in %s" % (rev, repo))
    if not re.fullmatch(r"[0-9a-f]{40}", out):
        raise SetupError("--rev %r does not resolve to one commit in %s" % (rev, repo))
    return out


def listing(repo, rev):
    out = git(repo, "ls-tree", "-r", "--name-only", rev)
    return {p for p in out.decode("utf-8", "surrogateescape").splitlines() if p}


def population(files):
    pop = []
    for path in files:
        if "__pycache__" in path or path.endswith((".pyc", ".pyo")):
            continue
        if path.startswith("tools/"):
            pop.append(path)
            continue
        for root in ("quality/counters/", "quality/"):
            if not path.startswith(root):
                continue
            rest = path[len(root):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
            break
    return sorted(set(pop))


# --------------------------------------------------------------------------
# ledger parsing
# --------------------------------------------------------------------------

def unfenced(text):
    """Lines outside ```/~~~ fences (a fenced row is documentation, not a ledger row)."""
    out, fence = [], None
    for line in text.splitlines():
        stripped = line.strip()
        if fence is None:
            match = re.match(r"^(`{3,}|~{3,})", stripped)
            if match:
                fence = match.group(1)[0] * 3
                continue
            out.append(line)
        elif stripped.startswith(fence):
            fence = None
    return out


def clean(cell):
    return cell.replace("`", "").replace("**", "").strip()


def norm_path(cell):
    path = clean(cell)
    if path.startswith("./"):
        path = path[2:]
    if path.startswith("/") or ".." in path.split("/"):
        return None
    path = LINE_SUFFIX.sub("", path)
    return path or None


def rows_of(text):
    """[(path, description, pointer_region_cells)] for every ledger row."""
    rows = []
    for line in unfenced(text):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if cells and all(SEPARATOR_CELL.match(c.strip()) for c in cells if c.strip()):
            continue
        path = norm_path(cells[0]) if cells else None
        if not path or "/" not in path:
            # header row, prose table, or a non-path first cell: not a ledger row
            continue
        desc = cells[1] if len(cells) > 1 else ""
        region = cells[2:] if len(cells) > 2 else []
        rows.append({"path": path, "desc": desc, "region": region, "cells": cells})
    return rows


def path_tokens(cell):
    """Repo paths named by a cell: backticked spans first, else bare path-shaped words."""
    spans = BACKTICK.findall(cell)
    if not spans:
        spans = [w.strip("()[]<>\"'").rstrip(".,;:") for w in re.split(r"[\s,;]+", cell)]
    out = []
    for span in spans:
        span = span.strip().split("#", 1)[0]
        if span.startswith("./"):
            span = span[2:]
        span = LINE_SUFFIX.sub("", span)
        if span and span not in out:
            out.append(span)
    return out


def names_basename(text, want):
    """True iff TEXT names WANT as a name, not as a fragment of a longer filename."""
    return re.search(NAME_BOUND % re.escape(want), text) is not None


def normalize(text):
    return " ".join(WORD.findall(text.lower()))


def bigrams(words):
    return [" ".join(words[i:i + 2]) for i in range(len(words) - 1)]


def path_words(path):
    """The words a path contributes: its basename and its directory names."""
    words = set(WORD.findall(os.path.basename(path).lower()))
    words |= set(WORD.findall(os.path.dirname(path).lower()))
    return words


def population_path_words(pop):
    """The naming vocabulary of the whole population: every word any instrument path
    contributes.  A phrase built only from these restates the lane's naming, not any
    one instrument's function."""
    words = set()
    for path in pop:
        words |= path_words(path)
    return words


# Closed-class English function words.  A two-word phrase made only of these carries
# no instrument-specific information ("nothing else" is not a description of anything).
FUNCTION_WORDS = frozenset("""the a an and or but of to in for with from into onto over
under per by at as is are was were be been being am do does did done have has had not no
nor none nothing all any some each every other others another such same own self this that
these those it its they them their he she his her we us our you your i me my one two three
four five many much more most less least few several if then else when while where which
who whom whose what why how because so than too very just only also even still yet ever
never always can could will would shall should may might must here there now once again
away back down out off up both either neither anything something everything someone anyone
everyone nobody nowhere everywhere anyway therefore thus hence via etc""".split())


def path_fragments(text):
    """Two-word sequences that occur inside a filesystem path in TEXT.

    "/usr/bin/xkbcli" contributes "usr bin".  Such a phrase is a path, not a
    description of what the instrument does.
    """
    frags = set()
    for match in re.finditer(r"[A-Za-z0-9_./-]*[/][A-Za-z0-9_./-]*", text):
        words = WORD.findall(match.group(0).lower())
        for index in range(len(words) - 1):
            frags.add(" ".join(words[index:index + 2]))
    return frags


# --------------------------------------------------------------------------
# measurement
# --------------------------------------------------------------------------

class Reader(object):
    """Committed bytes at one revision, read with `git show` only."""

    def __init__(self, repo, rev):
        self.repo = repo
        self.rev = rev
        self.files = listing(repo, rev)
        self._cache = {}

    def blob(self, path):
        if path not in self._cache:
            try:
                self._cache[path] = git(self.repo, "show", "%s:%s" % (self.rev, path))
            except SetupError:
                self._cache[path] = b""
        return self._cache[path]

    def text(self, path):
        return self.blob(path).decode("utf-8", "replace")


def measure(reader, ledger_text, ledger_rel=LEDGER_REL):
    """(counts, details) for one ledger text against the population at reader.rev."""
    pop = population(reader.files)
    in_pop = set(pop)
    population_words = population_path_words(pop)
    counts = dict(uncovered=0, dup=0, dangling=0, bad_pointer=0, self_pointer=0,
                  generic_desc=0)
    details = []
    seen = {}
    seen_desc = {}
    rows = rows_of(ledger_text)
    for row in rows:
        path = row["path"]
        if path not in in_pop:
            counts["dangling"] += 1
            details.append("dangling path=%s" % path)
            continue
        if path in seen:
            counts["dup"] += 1
            details.append("dup path=%s already-seen" % path)
            continue
        seen[path] = True

        # --- accountability pointer (the ledger's own grammar: cells 3..) -------
        targets = []
        for cell in row["region"]:
            for token in path_tokens(cell):
                if token not in targets:
                    targets.append(token)
        qualifying = []
        for token in targets:
            if token not in reader.files:
                continue
            body = reader.text(token)
            if names_basename(body, os.path.basename(path)):
                qualifying.append(token)
        # A peer instrument is not an accountability document: another tool's source
        # may name this basename in passing, but a tool cannot be accountable for a
        # sibling tool.  The pointer must land on a document, not on a sibling file.
        peer = [t for t in qualifying if t in in_pop and t != path]
        # The ledger under test, or the instrument's own file, names the instrument
        # only by accident — the ledger's bytes contain every basename — so neither
        # is ever an accountable target.
        circular = [t for t in qualifying if t in (ledger_rel, path)]
        accountable = [t for t in qualifying if t not in peer and t not in circular]

        # --- non-self pointer -------------------------------------------------
        # The pointer region is the row's accountability claim.  If the ledger (or
        # the instrument's own file) is named THERE, the claim is circular whatever
        # else the row names — a second accountable document does not launder it.
        pointer_self = []
        for cell in row["region"]:
            for token in path_tokens(cell):
                if "/" not in token:
                    continue
                if token in (ledger_rel, path) and token not in pointer_self:
                    pointer_self.append(token)
        # Any other cell may still be the row's only accountability claim: the frozen
        # control names the ledger in a cell that is not its pointer cell.  So the
        # wider scan applies to rows that designate no accountable target at all.
        wide_self = []
        for cell in row["cells"][1:]:
            for token in path_tokens(cell):
                if "/" not in token:
                    continue
                if token in (ledger_rel, path) and token not in wide_self:
                    wide_self.append(token)

        if pointer_self:
            counts["self_pointer"] += 1
            details.append("self_pointer path=%s target=%s" % (path, pointer_self[0]))
        elif accountable:
            # The row designates an accountable document; a mention of the ledger
            # elsewhere in the row is prose about what the instrument does, not a
            # claim of accountability.  It is recorded, not scored.
            if wide_self:
                details.append("note path=%s names-the-ledger-in-prose target=%s"
                               % (path, wide_self[0]))
        elif wide_self:
            counts["self_pointer"] += 1
            details.append("self_pointer path=%s target=%s" % (path, wide_self[0]))
        elif peer:
            counts["bad_pointer"] += 1
            details.append("bad_pointer path=%s pointer=%r reason=peer-instrument:%s" % (
                path, " | ".join(row["region"])[:100], peer[0]))
        else:
            counts["bad_pointer"] += 1
            details.append("bad_pointer path=%s pointer=%r reason=%s" % (
                path, " | ".join(row["region"])[:100],
                "no-target-names-the-instrument" if targets else "no-pointer-named"))

        # --- instrument-specific functional context ---------------------------
        desc = row["desc"].strip(EMPHASIS)
        words = normalize(desc).split()
        if len(row["cells"]) != 3:
            # Informational, not a defect: the ledger's own grammar is three cells,
            # but a wider row is still scored so that the defect it carries is named.
            details.append("note path=%s cells=%d" % (path, len(row["cells"])))
        reason = None
        if not desc or PLACEHOLDER.match(desc):
            reason = "empty-or-placeholder"
        elif desc in seen_desc:
            reason = "repeated-verbatim-of:%s" % seen_desc[desc]
        elif len(words) < MIN_DESC_WORDS:
            reason = "too-short:%d-words" % len(words)
        else:
            raw = reader.text(path)
            body = " " + normalize(raw) + " "
            frags = path_fragments(raw)
            own = path_words(path)
            bound = [phrase for phrase in bigrams(words) if " %s " % phrase in body]
            # A bound phrase carries instrument-specific functional context only if it
            # is not merely the instrument's own name, the lane's naming vocabulary, a
            # filesystem path, or a string of English function words.
            surviving = []
            for phrase in bound:
                phrase_words = set(phrase.split())
                if phrase_words <= own:
                    continue
                if phrase_words <= population_words:
                    continue
                if phrase in frags:
                    continue
                if phrase_words <= FUNCTION_WORDS:
                    continue
                surviving.append(phrase)
            if not bound:
                reason = "no-instrument-specific-phrase"
            elif not surviving:
                reason = "bound-only-by-name-path-or-function-words"
        if reason:
            counts["generic_desc"] += 1
            details.append("generic_desc path=%s reason=%s" % (path, reason))
        seen_desc.setdefault(desc, path)

    counts["uncovered"] = len(in_pop - set(seen))
    missing = sorted(in_pop - set(seen))
    for path in missing[:MAX_UNCOVERED_DETAILS]:
        details.append("uncovered path=%s" % path)
    if len(missing) > MAX_UNCOVERED_DETAILS:
        details.append("uncovered ... %d more paths not listed" % (
            len(missing) - MAX_UNCOVERED_DETAILS))
    counts["population"] = len(pop)
    counts["ledger_rows"] = len(rows)
    return counts, details


def summarise(counts, rev, ledger_rel=LEDGER_REL):
    met = (counts["population"] > 0
           and counts["ledger_rows"] == counts["population"]
           and not any(counts[k] for k in ("uncovered", "dup", "dangling", "bad_pointer",
                                           "self_pointer", "generic_desc")))
    line = ("C1_R52: population=%d ledger_rows=%d uncovered=%d dup=%d dangling=%d "
            "bad_pointer=%d self_pointer=%d generic_desc=%d verdict=%s rev=%s" % (
                counts["population"], counts["ledger_rows"], counts["uncovered"],
                counts["dup"], counts["dangling"], counts["bad_pointer"],
                counts["self_pointer"], counts["generic_desc"],
                "TARGET_MET" if met else "TARGET_MISSED", rev))
    return met, line


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

class Suite(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.passed = 0
        self.failed = []

    def check(self, name, ok, detail=""):
        if ok:
            self.passed += 1
            if self.verbose:
                print("ok   %s %s" % (name, detail))
        else:
            self.failed.append((name, detail))
            print("FAIL %s %s" % (name, detail))

    def report(self):
        total = self.passed + len(self.failed)
        if total != SELFTEST_CHECKS:
            self.failed.append(("selftest-count", "expected=%d got=%d" % (SELFTEST_CHECKS, total)))
            total = self.passed + len(self.failed)
        for name, detail in self.failed:
            print("FAILED: %s %s" % (name, detail))
        print("C1_R52_SELFTEST: %d/%d passed" % (self.passed, total))
        return 0 if not self.failed else 1


TOOL_ALPHA = """#!/usr/bin/env python3
\"\"\"alpha alpha -- the alpha watcher reads the widget registry and prints widget rows.\"\"\"

BIN = "/usr/bin/alpha-tool"

def main():
    print("widget rows")
"""
TOOL_BETA = """#!/usr/bin/env bash
# beta checker -- verifies the registry and prints verdicts for the widget plan.
echo "widget verdict"
"""
TOOL_DELTA = """#!/usr/bin/env python3
\"\"\"delta counter -- scores the registry rows of alpha.py and prints each verdict.\"\"\"
"""
SCORECARD = """# synthetic scorecard

- tools/alpha.py is the alpha watcher.
- tools/beta.sh is the beta checker.
- quality/counters/c1-delta.py is the delta counter.
"""
LEDGER_GREEN = """# synthetic ledger

| instrument | description | accountability pointer |
|---|---|---|
| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |
| `tools/beta.sh` | Verifies the registry and prints verdicts for the widget plan | `SCORECARD.md` |
| `quality/counters/c1-delta.py` | Scores the registry rows and prints the verdict for each widget | `SCORECARD.md` |
"""
LEDGER_SELF = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | "
    "`quality/tool-ledger.md` |")
LEDGER_SELF_ROW = LEDGER_GREEN.replace(
    "| `tools/beta.sh` | Verifies the registry and prints verdicts for the widget plan | `SCORECARD.md` |",
    "| `tools/beta.sh` | Verifies the registry and prints verdicts for the widget plan | "
    "`tools/beta.sh` |")
LEDGER_GENERIC = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | does things. | `SCORECARD.md` |")
LEDGER_NAME_ONLY = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | alpha alpha alpha alpha alpha alpha | `SCORECARD.md` |")
# The two escapes found by the C1Fixture peer seat: a description that quotes a
# filesystem path fragment out of the instrument's own bytes, and one that quotes the
# lane's naming vocabulary.  Neither carries functional context.
LEDGER_PATH_FRAGMENT = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | usr bin and nothing else at all here okay | `SCORECARD.md` |")
LEDGER_NAME_LAUNDER = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | alpha tools alpha tools and nothing more here okay | `SCORECARD.md` |")
LEDGER_DUP = LEDGER_GREEN.replace(
    "| `tools/beta.sh` | Verifies the registry and prints verdicts for the widget plan | `SCORECARD.md` |",
    "| `tools/beta.sh` | Verifies the registry and prints verdicts for the widget plan | `SCORECARD.md` |\n"
    "| `tools/beta.sh` | Verifies the registry and prints verdicts for the widget plan | `SCORECARD.md` |")
LEDGER_BADPTR = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `docs/missing.md` |")
LEDGER_PEER = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | "
    "`quality/counters/c1-delta.py` |")
# An honest row for an instrument whose job IS to read the ledger: the description
# names the ledger, the pointer designates an accountable document.  The mention is
# prose, not an accountability claim, so this row must pass.
LEDGER_LEDGER_READER = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Reads quality/tool-ledger.md and prints the widget registry "
    "rows for each instrument | `SCORECARD.md` |")
LEDGER_DANGLING = LEDGER_GREEN + (
    "| `tools/ghost.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |\n")
# The laundering case the peer seat found: the accountability pointer names the ledger
# AND an accountable document.  A second document must not launder a circular pointer.
LEDGER_LAUNDER = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | "
    "`quality/tool-ledger.md` and `SCORECARD.md` |")
# The same laundering split across two cells (a four-cell row).
LEDGER_LAUNDER_WIDE = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | "
    "`quality/tool-ledger.md` | `SCORECARD.md` |")
# The pointer may spell the ledger in another form.  These are load-bearing token
# cases: an exact-string comparison would miss the relative and anchored spellings.
LEDGER_SELF_RELATIVE = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | "
    "`./quality/tool-ledger.md` |")
LEDGER_SELF_ANCHOR = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | "
    "`quality/tool-ledger.md:1` |")
LEDGER_SELF_OWN_ROW = LEDGER_GREEN.replace(
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | `SCORECARD.md` |",
    "| `tools/alpha.py` | Watches the widget registry and prints widget rows | "
    "`tools/alpha.py` and `SCORECARD.md` |")
LEDGER_UNCOVERED = "\n".join(
    line for line in LEDGER_GREEN.splitlines() if "c1-delta.py" not in line) + "\n"
# The frozen control's shape: four cells, the ledger path named in the description cell,
# prose in the pointer cell.
LEDGER_CONTROL_SHAPE = """# control-shaped table

| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| tools/alpha.py | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |
"""


def fixture_repo(root):
    """A throwaway git repository holding a three-instrument population."""
    path = os.path.join(root, "fixture")
    os.makedirs(path, exist_ok=False)
    env = git_env()
    env["HOME"] = root
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull

    def run(*args):
        proc = subprocess.run(("git", "-C", path) + args, capture_output=True, env=env)
        if proc.returncode != 0:
            raise SetupError("fixture git %s failed: %s" % (
                " ".join(args), proc.stderr.decode("utf-8", "replace").strip()))
        return proc.stdout

    run("init", "-q")
    run("config", "user.name", "c1-r52-selftest")
    run("config", "user.email", "c1-r52-selftest@example.invalid")
    run("config", "commit.gpgsign", "false")
    top = run("rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != os.path.realpath(path):
        raise SetupError("fixture toplevel %r != %r" % (top, path))
    files = {
        "tools/alpha.py": TOOL_ALPHA,
        "tools/beta.sh": TOOL_BETA,
        "quality/counters/c1-delta.py": TOOL_DELTA,
        "SCORECARD.md": SCORECARD,
        "quality/tool-ledger.md": LEDGER_GREEN,
    }
    for rel, text in files.items():
        full = os.path.join(path, rel)
        os.makedirs(os.path.dirname(full) or path, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    run("add", "-A")
    run("commit", "-q", "-m", "fixture")
    return path, run("rev-parse", "HEAD").decode().strip()


def selftest(work, verbose=False):
    suite = Suite(verbose)
    root = tempfile.mkdtemp(prefix="c1-r52-selftest.", dir=work)
    try:
        repo, rev = fixture_repo(root)
        reader = Reader(repo, rev)

        def score(text):
            counts, details = measure(reader, text)
            met, line = summarise(counts, rev)
            return counts, met, line, details

        counts, met, line, _ = score(LEDGER_GREEN)
        suite.check("green-verdict", met, line)
        suite.check("green-population", counts["population"] == 3, str(counts["population"]))
        suite.check("green-rows", counts["ledger_rows"] == 3, str(counts["ledger_rows"]))
        for field in ("uncovered", "dup", "dangling", "bad_pointer", "self_pointer",
                      "generic_desc"):
            suite.check("green-%s-zero" % field, counts[field] == 0, str(counts[field]))

        counts, met, line, details = score(LEDGER_SELF)
        suite.check("self-verdict", not met, line)
        suite.check("self-pointer-count", counts["self_pointer"] == 1, str(counts["self_pointer"]))
        suite.check("self-pointer-detail",
                    any(d.startswith("self_pointer path=tools/alpha.py") for d in details),
                    " | ".join(details[:3]))

        counts, met, line, details = score(LEDGER_GENERIC)
        suite.check("generic-verdict", not met, line)
        suite.check("generic-desc-count", counts["generic_desc"] == 1, str(counts["generic_desc"]))
        suite.check("generic-desc-detail",
                    any(d.startswith("generic_desc path=tools/alpha.py") for d in details),
                    " | ".join(details[:3]))

        counts, met, line, _ = score(LEDGER_DUP)
        suite.check("dup-verdict", not met, line)
        suite.check("dup-count", counts["dup"] == 1, str(counts["dup"]))

        counts, met, line, _ = score(LEDGER_BADPTR)
        suite.check("badpointer-verdict", not met, line)
        suite.check("badpointer-count", counts["bad_pointer"] == 1, str(counts["bad_pointer"]))

        counts, met, line, _ = score(LEDGER_DANGLING)
        suite.check("dangling-verdict", not met, line)
        suite.check("dangling-count", counts["dangling"] == 1, str(counts["dangling"]))

        counts, met, line, _ = score(LEDGER_UNCOVERED)
        suite.check("uncovered-verdict", not met, line)
        suite.check("uncovered-count", counts["uncovered"] == 1, str(counts["uncovered"]))

        counts, met, line, details = score(LEDGER_CONTROL_SHAPE)
        suite.check("control-shape-verdict", not met, line)
        suite.check("control-shape-self-pointer", counts["self_pointer"] == 1,
                    str(counts["self_pointer"]))
        suite.check("control-shape-generic-desc", counts["generic_desc"] == 1,
                    str(counts["generic_desc"]))

        counts, met, line, details = score(LEDGER_SELF_ROW)
        suite.check("row-self-verdict", not met, line)
        suite.check("row-self-pointer-count", counts["self_pointer"] == 1,
                    str(counts["self_pointer"]))
        suite.check("row-self-pointer-detail",
                    any("self_pointer path=tools/beta.sh target=tools/beta.sh"
                        in d for d in details), " | ".join(details[:3]))

        counts, met, line, details = score(LEDGER_NAME_ONLY)
        suite.check("name-only-verdict", not met, line)
        suite.check("name-only-reason",
                    any("reason=bound-only-by-name-path-or-function-words" in d
                        for d in details), " | ".join(details[:3]))

        counts, met, line, details = score(LEDGER_PATH_FRAGMENT)
        suite.check("path-fragment-verdict", not met, line)
        suite.check("path-fragment-generic-desc", counts["generic_desc"] == 1,
                    str(counts["generic_desc"]))

        counts, met, line, details = score(LEDGER_NAME_LAUNDER)
        suite.check("name-launder-verdict", not met, line)
        suite.check("name-launder-generic-desc", counts["generic_desc"] == 1,
                    str(counts["generic_desc"]))

        counts, met, line, details = score(LEDGER_PEER)
        suite.check("peer-verdict", not met, line)
        suite.check("peer-bad-pointer-count", counts["bad_pointer"] == 1,
                    str(counts["bad_pointer"]))
        suite.check("peer-reason",
                    any("reason=peer-instrument:" in d for d in details),
                    " | ".join(details[:3]))

        counts, met, line, details = score(LEDGER_LEDGER_READER)
        suite.check("ledger-reader-verdict", met, line)
        suite.check("ledger-reader-self-pointer-zero", counts["self_pointer"] == 0,
                    str(counts["self_pointer"]))
        suite.check("ledger-reader-generic-desc-zero", counts["generic_desc"] == 0,
                    str(counts["generic_desc"]))
        suite.check("ledger-reader-note",
                    any("names-the-ledger-in-prose" in d for d in details),
                    " | ".join(details[:3]))

        counts, met, line, details = score(LEDGER_LAUNDER)
        suite.check("launder-verdict", not met, line)
        suite.check("launder-self-pointer-count", counts["self_pointer"] == 1,
                    str(counts["self_pointer"]))
        suite.check("launder-detail",
                    any("self_pointer path=tools/alpha.py target=quality/tool-ledger.md"
                        in d for d in details), " | ".join(details[:3]))

        counts, met, line, details = score(LEDGER_LAUNDER_WIDE)
        suite.check("launder-wide-verdict", not met, line)
        suite.check("launder-wide-self-pointer-count", counts["self_pointer"] == 1,
                    str(counts["self_pointer"]))

        for name, ledger_text, label in (
                ("relative-path", LEDGER_SELF_RELATIVE, "self-relative"),
                ("line-anchor", LEDGER_SELF_ANCHOR, "self-anchor"),
                ("own-row-path", LEDGER_SELF_OWN_ROW, "self-own-row")):
            counts, met, line, details = score(ledger_text)
            suite.check("%s-verdict" % label, not met, line)
            suite.check("%s-count" % label, counts["self_pointer"] == 1,
                        str(counts["self_pointer"]))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return suite.report()


def resolve_work(explicit):
    """Validate (and create) the scratch root the caller named.

    Measurement mode writes nothing into it; the --selftest mode builds its throwaway
    fixture repository under it.  A caller-named path that does not exist yet is
    created, as the lane's other counters do, so a driver that passes a fresh scratch
    path is not punished for it.
    """
    cand = explicit or os.environ.get("TMPDIR")
    if not cand:
        raise SetupError("--work <dir> or a TMPDIR outside %s is required"
                         % ", ".join(REFUSED_WORK_PREFIXES))
    real = os.path.realpath(cand)
    for bad in REFUSED_WORK_PREFIXES:
        if real == bad or real.startswith(bad + os.sep):
            raise SetupError("refusing work dir under %s (got %s)" % (bad, real))
    if os.path.exists(real) and not os.path.isdir(real):
        raise SetupError("--work %s exists and is not a directory" % real)
    os.makedirs(real, exist_ok=True)
    return real


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="PRED-C1-r52 draft: tracked tool ledger accountability")
    ap.add_argument("--repo", default=None)
    ap.add_argument("--rev", default=None)
    ap.add_argument("--ledger", default=None,
                    help="score this ledger file instead of the revision's own")
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    try:
        if args.selftest:
            work = resolve_work(args.work)
            return selftest(work, args.verbose)
        if not args.repo or not args.rev:
            raise SetupError("--repo and --rev are required (or use --selftest)")
        # The work root is validated and created if it does not exist, but nothing is
        # written into it: this counter reads committed bytes with `git show` and needs
        # no scratch.  The validation keeps the harness contract honest and refuses the
        # /tmp family.
        resolve_work(args.work)
        repo = os.path.abspath(args.repo)
        if not os.path.isdir(repo):
            raise SetupError("--repo %s is not a directory" % repo)
        rev = resolve_rev(repo, args.rev)
        reader = Reader(repo, rev)
        if args.ledger:
            with open(args.ledger, "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
            ledger_rel = LEDGER_REL
        else:
            if LEDGER_REL not in reader.files:
                print("C1_R52: verdict=TARGET_MISSED ledger=absent population=%d rev=%s"
                      % (len(population(reader.files)), rev))
                return 1
            text = reader.text(LEDGER_REL)
            ledger_rel = LEDGER_REL
        counts, details = measure(reader, text, ledger_rel)
        for detail in details:
            print("detail: %s" % detail)
        met, line = summarise(counts, rev, ledger_rel)
        print(line)
        return 0 if met else 1
    except SetupError as exc:
        print("C1_R52: setup=error detail=%s" % exc, file=sys.stderr)
        return 2
    except OSError as exc:
        print("C1_R52: setup=error detail=%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
