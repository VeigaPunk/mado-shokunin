#!/usr/bin/env python3
"""check-tool-ledger.py -- PRED-C1-r51 gate: the tracked lane-level tool ledger is complete.

Round-50 w2 `RevLedgerR50` found that the wave-seat tool ledger missed two tracked tools
(`tools/mado-hostguard.py`, `tools/mado-keysym.py`) and that no lane-level ledger or checker
exists. This gate reads `quality/tool-ledger.md` and the population of instruments at one
committed revision and answers one question: does every instrument have exactly one row, a
non-empty description, and an accountability pointer that resolves?

Population (derived from the tree at --rev, never from the ledger)
    files under `tools/` (any path below it, any extension)
  + `quality/*.py`             (direct children only)
  + `quality/counters/*.py`    (direct children only)
Only blobs count (a gitlink or tree entry is not a file). `quality/tool-ledger.md` itself is
not an instrument and carries no row.

Ledger rows (fenced code blocks are ignored; header and `|---|` separator rows are skipped)
    | `<path>` | <description> | `<pointer>` |
  path        exact repo-relative path, backticked or bare; must equal a population path.
  description one line, must carry a letter or digit; `-`, `?`, `TBD`, `TODO`, `N/A`, `none`
              count as empty.
  pointer     one or more backticked repo paths (`path`, `path:N`, `path:N-M` -- a line
              suffix is stripped). Every named path must be a file at --rev and at least one
              must name the row file's basename in its bytes -- as a name, not as a fragment of
              a longer filename: the ledger names who is accountable for the instrument, and
              that accountability must be readable.

Findings  (each printed as `LEDGER-ROW reason=<r> path=<p> detail=<d>` before the summary)
    uncovered        population path with no row
    dangling         row whose path is not in the population, a repeated path, or a
                     malformed row (not exactly three cells)
    bad_pointer      pointer names no existing file, or none of the named files contains the
                     row file's basename
    empty_desc       description is blank or a placeholder
A dangling row is not also scored for pointer or description: one broken row, one finding.

Summary -- always the last line; the six frozen fields are always present:
    LEDGER: population=<P> ledger_rows=<R> uncovered=<n> dangling=<n> bad_pointer=<n> \
empty_desc=<n> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>
An absent ledger prints instead:
    LEDGER: population=<P> verdict=TARGET_MISSED ledger=absent rev=<sha>

Exit: 0 TARGET_MET (P>0, R==P and all four counters 0); 1 TARGET_MISSED (including an absent
ledger and an empty population); 2 setup or usage error (unreadable --rev or --repo, a ledger
that is not UTF-8, a refused work dir).

Usage::

    check-tool-ledger.py --repo <lane> --rev <rev> [--verbose]
    check-tool-ledger.py --selftest [--work <dir>] [--verbose]

Reads committed bytes only (read-only git); writes nothing, except `--selftest`, which builds
throwaway fixture repositories in a private directory under --work/TMPDIR and removes it.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

LEDGER = "quality/tool-ledger.md"
PRED = "PRED-C1-r51"

# The exact number of assertions --selftest must make: a case that silently disappears (an
# env-dependent skip, a removed fixture) must fail the run, not shrink it.
SELFTEST_CHECKS = 50

REFUSED_WORK_PREFIXES = ("/tmp", "/var/tmp", "/dev/shm")
GIT_ENV_KEYS = ("PATH", "SYSTEMROOT")

QUALITY_PY = re.compile(r"^quality/[^/]+\.py$")
COUNTERS_PY = re.compile(r"^quality/counters/[^/]+\.py$")
SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")
HEADER_CELLS = frozenset({"path", "file", "instrument", "tool", "artifact"})
LINE_SUFFIX = re.compile(r":(?:\d+)(?:-\d+)?$")
PATH_TOKEN = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._#-]+)+$")
BACKTICK = re.compile(r"`([^`\n]+)`")
PLACEHOLDERS = frozenset({"-", "--", "---", "—", "–", "?", "tbd", "todo", "n/a", "na",
                          "none", "empty", "..."})
SAFE = re.compile(r"[^A-Za-z0-9._/=,:@+-]+")


class GateError(Exception):
    """The question cannot be answered (exit 2)."""


# --------------------------------------------------------------------------
# read-only git
# --------------------------------------------------------------------------

def git_env(home=None):
    env = {k: os.environ[k] for k in GIT_ENV_KEYS if k in os.environ}
    env.setdefault("PATH", "/usr/bin:/bin")
    env["HOME"] = home or os.environ.get("HOME") or "/nonexistent"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["LC_ALL"] = "C"
    return env


def run_git(repo, args):
    cmd = ["git", "-C", repo] + list(args)
    proc = subprocess.run(cmd, capture_output=True, env=git_env())
    if proc.returncode != 0:
        raise GateError("%s exited %d: %s" % (
            " ".join(cmd), proc.returncode,
            proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def check_repo(repo):
    if not os.path.isdir(repo):
        raise GateError("--repo %r is not a directory" % repo)
    proc = subprocess.run(["git", "-C", repo, "rev-parse", "--git-dir"],
                          capture_output=True, env=git_env())
    if proc.returncode != 0:
        raise GateError("--repo %r is not a git repository" % repo)


def resolve_rev(repo, rev):
    if not rev or not rev.strip():
        raise GateError("--rev is empty")
    out = run_git(repo, ["rev-parse", "--verify", "--end-of-options",
                         rev + "^{commit}"])
    sha = out.decode("utf-8", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40}([0-9a-f]{24})?", sha):
        raise GateError("--rev %r did not resolve to one commit (%r)" % (rev, sha))
    return sha


def tree(repo, sha):
    """path -> oid for every blob at SHA (recursive; non-blob entries are dropped)."""
    out = run_git(repo, ["ls-tree", "-r", "-z", sha])
    blobs = {}
    for rec in out.split(b"\0"):
        if not rec:
            continue
        head, sep, path = rec.partition(b"\t")
        if not sep:
            continue
        fields = head.split()
        if len(fields) < 3 or fields[1] != b"blob":
            continue
        blobs[path.decode("utf-8", "surrogateescape")] = fields[2].decode("ascii")
    return blobs


def blob(repo, sha, path):
    try:
        return run_git(repo, ["show", "%s:%s" % (sha, path)])
    except GateError as exc:
        raise GateError("cannot read %s at %s: %s" % (path, sha, exc))


# --------------------------------------------------------------------------
# population and ledger
# --------------------------------------------------------------------------

def is_population(path):
    if path.startswith("tools/"):
        return True
    return bool(QUALITY_PY.match(path) or COUNTERS_PY.match(path))


def population(blobs):
    return sorted(p for p in blobs if is_population(p))


def unfenced(text):
    """Lines outside ```/~~~ fences (a fenced row is documentation, not a ledger row)."""
    out, fence = [], None
    for line in text.splitlines():
        stripped = line.strip()
        if fence is None:
            m = re.match(r"^(`{3,}|~{3,})", stripped)
            if m:
                fence = m.group(1)[0] * 3
                continue
            out.append(line)
        else:
            if stripped.startswith(fence):
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


def description_empty(cell):
    text = clean(cell)
    text = re.sub(r"^[>*_~]+|[>*_~]+$", "", text).strip()
    if not text:
        return True
    if text.lower() in PLACEHOLDERS:
        return True
    return not any(ch.isalnum() for ch in text)


def pointer_tokens(cell):
    """Repo paths named by a pointer cell: backticked spans, else bare path-shaped words."""
    spans = BACKTICK.findall(cell)
    if not spans:
        spans = []
        for word in re.split(r"[\s,;]+", cell):
            word = word.strip("()[]<>\"'")
            word = word.rstrip(".,;:")
            if PATH_TOKEN.match(word) or PATH_TOKEN.match(LINE_SUFFIX.sub("", word)):
                spans.append(word)
    out = []
    for span in spans:
        span = span.strip()
        span = span.split("#", 1)[0]
        path = norm_path("`%s`" % span) if span else None
        if path and path not in out:
            out.append(path)
    return out


def parse_rows(lines):
    """[(lineno, path, description, pointer_cell)] plus a list of malformed row numbers."""
    rows, malformed, seen = [], [], False
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = stripped.strip("|").split("|")
        if not seen:
            # The table header is the first pipe row; its first cell is a label, not a path.
            if cells and clean(cells[0]).lower() in HEADER_CELLS:
                seen = True
                continue
        seen = True
        if cells and all(SEPARATOR_CELL.match(c.strip()) for c in cells if c.strip()):
            if any(c.strip() for c in cells):
                continue
        if len(cells) != 3:
            malformed.append((lineno, len(cells)))
            continue
        rows.append((lineno, cells[0], cells[1], cells[2]))
    return rows, malformed


def basename(path):
    return path.rsplit("/", 1)[-1]


def names_basename(text, want):
    """True iff TEXT names WANT as a name, not as a fragment of a longer filename."""
    rx = re.compile(r"(?<![A-Za-z0-9._-])" + re.escape(want) + r"(?![A-Za-z0-9_-])")
    return rx.search(text) is not None


def evaluate(pop, text, blobs, repo, sha):
    """(rows, uncovered, dangling, bad_pointer, empty_desc, findings)."""
    lines = unfenced(text)
    rows, malformed = parse_rows(lines)
    findings = []

    covered = {}
    dangling = 0
    for lineno, cell, _desc, _ptr in rows:
        path = norm_path(cell)
        if path is None or path not in pop:
            dangling += 1
            findings.append(("dangling", clean(cell) or "-", "line-%d" % lineno))
            continue
        if path in covered:
            dangling += 1
            findings.append(("dangling", path, "row-duplicate-line-%d" % lineno))
            continue
        covered[path] = (lineno, cell, _desc, _ptr)
    for lineno, ncells in malformed:
        dangling += 1
        findings.append(("dangling", "-", "row-malformed-cells-%d-line-%d" % (ncells, lineno)))

    uncovered = [p for p in pop if p not in covered]
    for path in uncovered:
        findings.append(("uncovered", path, "no-row"))

    empty_desc = 0
    bad_pointer = 0
    cache = {}
    for path, (_lineno, _cell, desc, ptr) in sorted(covered.items()):
        if description_empty(desc):
            empty_desc += 1
            findings.append(("empty_desc", path, "blank-or-placeholder"))
        tokens = pointer_tokens(ptr)
        if not tokens:
            bad_pointer += 1
            findings.append(("bad_pointer", path, "no-pointer-named"))
            continue
        missing = [t for t in tokens if t not in blobs]
        if missing:
            bad_pointer += 1
            findings.append(("bad_pointer", path, "pointer-missing:%s" % missing[0]))
            continue
        want = basename(path)
        hits = False
        for token in tokens:
            if token not in cache:
                try:
                    cache[token] = blob(repo, sha, token).decode("utf-8", "replace")
                except GateError:
                    cache[token] = ""
            if names_basename(cache[token], want):
                hits = True
                break
        if not hits:
            bad_pointer += 1
            findings.append(("bad_pointer", path, "pointer-lacks-basename:%s" % tokens[0]))

    findings.sort(key=lambda f: (f[0], f[1], f[2]))
    return len(rows), uncovered, dangling, bad_pointer, empty_desc, findings


def safe(text):
    return SAFE.sub("_", text)[:120]


def run_check(args):
    check_repo(args.repo)
    sha = resolve_rev(args.repo, args.rev)
    blobs = tree(args.repo, sha)
    pop = population(blobs)

    if LEDGER not in blobs:
        print("LEDGER: population=%d verdict=TARGET_MISSED ledger=absent rev=%s"
              % (len(pop), sha))
        return 1

    try:
        text = blob(args.repo, sha, LEDGER).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise GateError("%s at %s is not UTF-8: %s" % (LEDGER, sha, exc))

    rowcount, uncovered, dangling, bad_pointer, empty_desc, findings = evaluate(
        set(pop), text, blobs, args.repo, sha)

    for reason, path, detail in findings:
        print("LEDGER-ROW reason=%s path=%s detail=%s"
              % (reason, safe(path), safe(detail)))

    met = (len(pop) > 0 and rowcount == len(pop) and not uncovered
           and dangling == 0 and bad_pointer == 0 and empty_desc == 0)
    print("LEDGER: population=%d ledger_rows=%d uncovered=%d dangling=%d "
          "bad_pointer=%d empty_desc=%d verdict=%s rev=%s"
          % (len(pop), rowcount, len(uncovered), dangling, bad_pointer, empty_desc,
             "TARGET_MET" if met else "TARGET_MISSED", sha))
    return 0 if met else 1


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

class Suite:
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
            self.failed.append(("selftest-count",
                                "expected=%d got=%d" % (SELFTEST_CHECKS, total)))
            total = self.passed + len(self.failed)
        for name, detail in self.failed:
            print("FAILED: %s %s" % (name, detail))
        print("LEDGER_SELFTEST: %d/%d passed" % (self.passed, total))
        return 0 if not self.failed else 1


def home_roots():
    roots = []
    try:
        import pwd
        cand = pwd.getpwuid(os.getuid()).pw_dir
    except (ImportError, KeyError, OSError):
        cand = None
    for home in (os.environ.get("HOME"), cand):
        if not home or not home.strip():
            continue
        real = os.path.realpath(home)
        if real != os.sep and real not in roots:
            roots.append(real)
    return roots


def resolve_work(explicit):
    cand = explicit or os.environ.get("TMPDIR")
    if not cand:
        raise GateError("--selftest needs --work <dir> or a TMPDIR outside /tmp, /var/tmp, "
                        "/dev/shm and the home directory")
    real = os.path.realpath(cand)
    for bad in REFUSED_WORK_PREFIXES:
        if real == bad or real.startswith(bad + os.sep):
            raise GateError("refusing work dir under %s (got %s): use a scratch filesystem"
                            % (bad, real))
    for home in home_roots():
        if real == home or real.startswith(home + os.sep):
            raise GateError("refusing work dir inside the home directory (got ~%s)" %
                            real[len(home):])
    os.makedirs(real, exist_ok=True)
    return tempfile.mkdtemp(prefix="ledger-selftest.", dir=real)


class Fixture:
    """A throwaway git repository holding a population and a ledger."""

    def __init__(self, root, name):
        self.path = os.path.join(root, name)
        os.makedirs(self.path, exist_ok=False)
        self.home = os.path.join(root, "home")
        os.makedirs(self.home, exist_ok=True)
        self.env = git_env(self.home)
        self.env["TMPDIR"] = root
        self.git("init", "-q")
        self.git("config", "user.name", "fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        top = self.git("rev-parse", "--show-toplevel").decode().strip()
        if os.path.realpath(top) != os.path.realpath(self.path):
            raise GateError("fixture toplevel %r != %r" % (top, self.path))

    def git(self, *args):
        proc = subprocess.run(["git", "-C", self.path] + list(args),
                              capture_output=True, env=self.env)
        if proc.returncode != 0:
            raise GateError("fixture git %s failed: %s" % (
                " ".join(args), proc.stderr.decode("utf-8", "replace").strip()))
        return proc.stdout

    def write(self, path, content):
        full = os.path.join(self.path, path)
        os.makedirs(os.path.dirname(full) or self.path, exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)

    def commit(self, files, message):
        for path, content in files.items():
            self.write(path, content)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD").decode().strip()


def ledger(rows, header=True):
    out = ["# fixture tool ledger", ""]
    if header:
        out.append("| Path | Description | Accountability pointer |")
        out.append("| --- | --- | --- |")
    for cells in rows:
        out.append("| %s | %s | %s |" % cells)
    return "\n".join(out) + "\n"


NOTES = "alpha-tool.py zeta.sh check-a.py c1-x.py live in this file\n"
NOTES_PATH = "quality/notes.md"  # not a population file: quality/*.py only

BASE_FILES = {
    "tools/alpha-tool.py": "# alpha\n",
    "tools/zeta.sh": "#!/bin/sh\n",
    "quality/check-a.py": "# check\n",
    "quality/counters/c1-x.py": "# counter\n",
    NOTES_PATH: NOTES,
}

GOOD_ROWS = [
    ("`tools/alpha-tool.py`", "alpha instrument", "`quality/notes.md`"),
    ("`tools/zeta.sh`", "zeta shell instrument", "`quality/notes.md:12`"),
    ("`quality/check-a.py`", "check a", "`quality/notes.md:3-5`"),
    ("quality/counters/c1-x.py", "counter x", "quality/notes.md"),
]


def files(rows=None, with_ledger=True):
    out = dict(BASE_FILES)
    if with_ledger:
        out[LEDGER] = ledger(GOOD_ROWS if rows is None else rows)
    return out


def invoke(repo, rev, work, extra=()):
    proc = subprocess.run(
        [sys.executable, "-I", os.path.abspath(__file__),
         "--repo", repo, "--rev", rev] + list(extra),
        capture_output=True, env=git_env(os.path.join(work, "home")), text=True)
    return proc.returncode, proc.stdout


def summary(out):
    for line in reversed(out.splitlines()):
        if line.startswith("LEDGER:"):
            return line
    return ""


def selftest(work, verbose=False):
    suite = Suite(verbose)

    # G -- the green ledger: every population file covered once, every pointer resolvable.
    g = Fixture(work, "green")
    gsha = g.commit(files(), "green ledger")
    rc, out = invoke(g.path, gsha, work)
    line = summary(out)
    suite.check("green-exit-0", rc == 0, "rc=%d %s" % (rc, line))
    suite.check("green-summary",
                line == ("LEDGER: population=4 ledger_rows=4 uncovered=0 dangling=0 "
                         "bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=%s" % gsha),
                line)
    suite.check("green-no-findings", "LEDGER-ROW " not in out, out.strip()[:120])
    suite.check("green-uses-sha", ("rev=%s" % gsha) in line, line)

    # A -- (control a) a population file with no row is uncovered.
    a = Fixture(work, "omitted")
    asha = a.commit(files(GOOD_ROWS[:3]), "one file omitted")
    rc, out = invoke(a.path, asha, work)
    suite.check("control-a-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("control-a-uncovered", "uncovered=1" in summary(out)
                and "ledger_rows=3" in summary(out), summary(out))
    suite.check("control-a-names-path",
                "LEDGER-ROW reason=uncovered path=quality/counters/c1-x.py" in out,
                out.strip()[:160])

    # B -- (control b) a pointer file that exists but never names the instrument.
    b = Fixture(work, "bad-pointer")
    rows = list(GOOD_ROWS)
    rows[0] = ("`tools/alpha-tool.py`", "alpha instrument", "`quality/check-a.py`")
    bsha = b.commit(files(rows), "pointer lacks basename")
    rc, out = invoke(b.path, bsha, work)
    suite.check("control-b-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("control-b-bad-pointer", "bad_pointer=1" in summary(out), summary(out))
    suite.check("control-b-detail", "pointer-lacks-basename:quality/check-a.py" in out,
                out.strip()[:160])

    # B2 -- a decoy that carries the basename only as a fragment of a longer filename.
    b2 = Fixture(work, "decoy-substring")
    rows = list(GOOD_ROWS)
    rows[0] = ("`tools/alpha-tool.py`", "alpha instrument", "`quality/decoy.md`")
    files_b2 = files(rows)
    files_b2["quality/decoy.md"] = "mentions not-alpha-tool.py and nothing else\n"
    b2sha = b2.commit(files_b2, "decoy substring")
    rc, out = invoke(b2.path, b2sha, work)
    suite.check("decoy-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("decoy-bad-pointer", "bad_pointer=1" in summary(out)
                and "pointer-lacks-basename:quality/decoy.md" in out, out.strip()[:160])

    # C -- (control c) an empty description.
    c = Fixture(work, "empty-desc")
    rows = list(GOOD_ROWS)
    rows[1] = ("`tools/zeta.sh`", "-", "`quality/notes.md`")
    csha = c.commit(files(rows), "empty description")
    rc, out = invoke(c.path, csha, work)
    suite.check("control-c-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("control-c-empty-desc", "empty_desc=1" in summary(out), summary(out))

    # C2 -- whitespace is not a description.
    c2 = Fixture(work, "blank-desc")
    rows = list(GOOD_ROWS)
    rows[1] = ("`tools/zeta.sh`", "   ", "`quality/notes.md`")
    c2sha = c2.commit(files(rows), "whitespace description")
    rc, out = invoke(c2.path, c2sha, work)
    suite.check("blank-desc-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("blank-desc-empty", "empty_desc=1" in summary(out), summary(out))

    # D -- (control d) a row for a file that is not in the population.
    d = Fixture(work, "dangling")
    rows = list(GOOD_ROWS) + [("`tools/ghost.py`", "ghost", "`quality/notes.md`")]
    dsha = d.commit(files(rows), "dangling row")
    rc, out = invoke(d.path, dsha, work)
    suite.check("control-d-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("control-d-dangling", "dangling=1" in summary(out)
                and "ledger_rows=5" in summary(out), summary(out))

    # E -- (control e) no ledger at all: the round-51 base shape.
    e = Fixture(work, "absent")
    esha = e.commit(files(with_ledger=False), "no ledger")
    rc, out = invoke(e.path, esha, work)
    suite.check("control-e-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("control-e-absent",
                summary(out) == ("LEDGER: population=4 verdict=TARGET_MISSED ledger=absent "
                                 "rev=%s" % esha),
                summary(out))

    # F -- a pointer naming a file that does not exist is a bad pointer.
    f = Fixture(work, "pointer-missing")
    rows = list(GOOD_ROWS)
    rows[2] = ("`quality/check-a.py`", "check a", "`quality/nope.py`")
    fsha = f.commit(files(rows), "missing pointer")
    rc, out = invoke(f.path, fsha, work)
    suite.check("pointer-missing-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("pointer-missing-bad", "bad_pointer=1" in summary(out)
                and "pointer-missing:quality/nope.py" in out, out.strip()[:160])

    # F2 -- a pointer may not leave the repository: absolute and `..` paths are bad pointers.
    f2 = Fixture(work, "pointer-escapes")
    rows = list(GOOD_ROWS)
    rows[0] = ("`tools/alpha-tool.py`", "alpha instrument", "`/etc/hostname`")
    rows[1] = ("`tools/zeta.sh`", "zeta shell instrument", "`../outside.md`")
    f2sha = f2.commit(files(rows), "escaping pointers")
    rc, out = invoke(f2.path, f2sha, work)
    suite.check("escape-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("escape-bad-pointer", "bad_pointer=2" in summary(out)
                and "no-pointer-named" in out, out.strip()[:160])

    # G2 -- a repeated row for one file is not "exactly once": the second occurrence dangles.
    g2 = Fixture(work, "duplicate")
    rows = list(GOOD_ROWS) + [("`tools/alpha-tool.py`", "alpha again", "`quality/notes.md`")]
    g2sha = g2.commit(files(rows), "duplicate row")
    rc, out = invoke(g2.path, g2sha, work)
    suite.check("duplicate-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("duplicate-dangling", "dangling=1" in summary(out)
                and "row-duplicate-line-9" in out, out.strip()[:160])

    # H -- a malformed row (two cells) cannot be a ledger row.
    h = Fixture(work, "malformed")
    text = ledger(GOOD_ROWS) + "| `tools/alpha-tool.py` | no pointer |\n"
    files_h = dict(BASE_FILES)
    files_h[LEDGER] = text
    hsha = h.commit(files_h, "malformed row")
    rc, out = invoke(h.path, hsha, work)
    suite.check("malformed-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("malformed-dangling", "dangling=1" in summary(out)
                and "row-malformed-cells-2" in out, out.strip()[:160])

    # H2 -- a four-cell row is malformed, not a row that silently drops a column.
    h2 = Fixture(work, "malformed-wide")
    files_h2 = dict(BASE_FILES)
    files_h2[LEDGER] = ledger(GOOD_ROWS) + (
        "| `tools/alpha-tool.py` | dup | `quality/notes.md` | stray |\n")
    h2sha = h2.commit(files_h2, "four-cell row")
    rc, out = invoke(h2.path, h2sha, work)
    suite.check("malformed-wide-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("malformed-wide-dangling", "dangling=1" in summary(out)
                and "row-malformed-cells-4" in out, out.strip()[:160])

    # I -- an empty ledger table leaves the whole population uncovered.
    i = Fixture(work, "empty-table")
    files_i = dict(BASE_FILES)
    files_i[LEDGER] = ledger([])
    isha = i.commit(files_i, "empty table")
    rc, out = invoke(i.path, isha, work)
    suite.check("empty-table-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("empty-table-uncovered", "ledger_rows=0 uncovered=4" in summary(out),
                summary(out))

    # J -- a fenced row is documentation, not a ledger row: the file stays uncovered.
    j = Fixture(work, "fenced")
    text = ledger(GOOD_ROWS[:3]) + "\n```\n" + "| `quality/counters/c1-x.py` | fenced | " \
        "`quality/notes.md` |\n```\n"
    files_j = dict(BASE_FILES)
    files_j[LEDGER] = text
    jsha = j.commit(files_j, "fenced row")
    rc, out = invoke(j.path, jsha, work)
    suite.check("fenced-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("fenced-uncovered", "uncovered=1" in summary(out)
                and "path=quality/counters/c1-x.py" in out, out.strip()[:160])

    # K -- committed bytes only: a garbage worktree ledger does not change the verdict.
    k = Fixture(work, "worktree-invisible")
    ksha = k.commit(files(), "green ledger")
    k.write(LEDGER, "this worktree copy is not the ledger\n")
    rc, out = invoke(k.path, ksha, work)
    suite.check("worktree-not-read", rc == 0, summary(out))

    # K2 -- --rev pins the bytes: the same repo is absent one commit earlier.
    k2 = Fixture(work, "rev-pins")
    old = k2.commit(files(with_ledger=False), "no ledger yet")
    new = k2.commit({LEDGER: ledger(GOOD_ROWS)}, "ledger lands")
    rc_old, out_old = invoke(k2.path, old, work)
    rc_new, out_new = invoke(k2.path, new, work)
    suite.check("rev-pins-bytes", rc_old == 1 and rc_new == 0
                and "ledger=absent" in summary(out_old), "%s | %s"
                % (summary(out_old), summary(out_new)))

    # L -- the population globs exactly as the predicate states them.
    l = Fixture(work, "globs")
    rows_l = [("`tools/sub/deep.py`", "deep tool", "`quality/notes.md`"),
              ("`quality/y.py`", "top-level py", "`quality/notes.md`")]
    files_l = {
        "tools/sub/deep.py": "# deep\n",
        "quality/y.py": "# y\n",
        "quality/sub/x.py": "# not a direct child\n",
        "quality/readme.md": "not a .py\n",
        "quality/counters/deep/ignored.py": "# not a direct child\n",
        "quality/notes.md": "deep.py y.py\n",
        LEDGER: ledger(rows_l),
    }
    lsha = l.commit(files_l, "glob fixture")
    rc, out = invoke(l.path, lsha, work)
    suite.check("population-globs", rc == 0 and "population=2 ledger_rows=2" in summary(out),
                summary(out))

    # M -- an empty population cannot be met: nothing to cover is not coverage.
    m = Fixture(work, "no-population")
    files_m = {LEDGER: ledger([])}
    msha = m.commit(files_m, "ledger only")
    rc, out = invoke(m.path, msha, work)
    suite.check("empty-population-exit-1", rc == 1, "rc=%d %s" % (rc, summary(out)))
    suite.check("empty-population-zero", "population=0" in summary(out), summary(out))

    # N -- usage and setup errors are exit 2, never a silent pass.
    child_home = os.path.join(work, "child-home")
    os.makedirs(child_home, exist_ok=True)
    for label, argv in (
            ("no-repo", ["--rev", "HEAD"]),
            ("no-rev", ["--repo", g.path]),
            ("selftest-plus-repo", ["--selftest", "--repo", g.path]),
            ("work-without-selftest", ["--repo", g.path, "--rev", "HEAD",
                                       "--work", work]),
    ):
        proc = subprocess.run([sys.executable, "-I", os.path.abspath(__file__)] + argv,
                              capture_output=True, env=git_env(child_home), text=True)
        suite.check("usage-%s-exit-2" % label, proc.returncode == 2,
                    "rc=%d" % proc.returncode)

    proc = subprocess.run([sys.executable, "-I", os.path.abspath(__file__),
                           "--repo", g.path, "--rev", "0" * 40],
                          capture_output=True, env=git_env(child_home), text=True)
    suite.check("unresolvable-rev-exit-2", proc.returncode == 2, "rc=%d" % proc.returncode)

    proc = subprocess.run([sys.executable, "-I", os.path.abspath(__file__),
                           "--repo", os.path.join(work, "not-a-repo"),
                           "--rev", "HEAD"],
                          capture_output=True, env=git_env(child_home), text=True)
    suite.check("not-a-repo-exit-2", proc.returncode == 2, "rc=%d" % proc.returncode)

    # O -- the scratch rule: no work dir under /tmp, /var/tmp, /dev/shm or the home directory.
    for bad_dir in REFUSED_WORK_PREFIXES:
        cand = os.path.join(bad_dir, "ledger-selftest")
        try:
            resolve_work(cand)
            refused, detail = False, "accepted"
        except GateError as exc:
            refused, detail = True, str(exc)[:60]
        suite.check("refuse-work-%s" % bad_dir.strip("/").replace("/", "-"), refused, detail)

    roots = home_roots()
    accepted = []
    for home in roots:
        for cand in (home, os.path.join(home, "ledger-selftest")):
            try:
                resolve_work(cand)
                accepted.append(cand)
            except GateError:
                pass
    suite.check("refuse-work-home", not accepted,
                "roots=%d accepted=%s" % (len(roots), accepted[:2]))

    # P -- TMPDIR is honoured when --work is not given.
    saved = os.environ.get("TMPDIR")
    os.environ["TMPDIR"] = work
    try:
        made = resolve_work(None)
        try:
            suite.check("tmpdir-honoured",
                        os.path.realpath(made).startswith(os.path.realpath(work) + os.sep),
                        made)
        finally:
            shutil.rmtree(made, ignore_errors=True)
    finally:
        if saved is None:
            os.environ.pop("TMPDIR", None)
        else:
            os.environ["TMPDIR"] = saved

    return suite.report()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="check-tool-ledger.py",
        description="PRED-C1-r51: score the tracked lane-level tool ledger at one revision.")
    parser.add_argument("--repo", help="git repository (read-only)")
    parser.add_argument("--rev", help="revision whose committed bytes are scored")
    parser.add_argument("--selftest", action="store_true", help="run the hermetic fixture suite")
    parser.add_argument("--work", help="scratch dir for --selftest (or TMPDIR); /tmp is refused")
    parser.add_argument("--verbose", action="store_true",
                        help="print every passing selftest case / every finding")
    args = parser.parse_args(argv)

    if args.selftest:
        if args.repo or args.rev:
            parser.error("--selftest takes only --work/--verbose")
        try:
            work = resolve_work(args.work)
        except GateError as exc:
            sys.stderr.write("check-tool-ledger.py: %s\n" % exc)
            return 2
        try:
            return selftest(work, args.verbose)
        finally:
            shutil.rmtree(work, ignore_errors=True)

    if args.work:
        parser.error("--work is only for --selftest")
    if not args.repo or not args.rev:
        parser.error("--repo and --rev are required (or use --selftest)")
    try:
        return run_check(args)
    except GateError as exc:
        sys.stderr.write("check-tool-ledger.py: %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
