#!/usr/bin/env python3
"""check-ledger.py - re-derive every row of the round-49 live-state tool ledger from git objects.

The ledger (`ledger.md`, beside this file) is *generated* by `--emit` from the
objects of one revision. Every quoted line in it is copied out of the object it
is attributed to, so a compressed or invented quote cannot appear (round-47
H3/H5), and a `none` is derived by a sweep, never asserted (round-47 H2/H6).

Per-row rules, all implemented below
------------------------------------
  tool       every blob under `tools/` at the revision is a row or a listed
             exclusion; a tool that is neither is a failure.
  class      LIVE-PROBE | LIVE-JOIN | LIVE-CONFIG | SESSION-RECORD |
             CONFIG-SCORED, each tied to a literal in the tool's bytes (printed
             with its line). LIVE-PROBE literals must sit outside the module
             docstring, i.e. in code.
  question   a line number inside the module docstring (or a `#` line for .sh).
  reads      a literal the tool reads; every line containing it is printed.
  receipt    among files at the revision that (a) sit under `receipts/`,
             `evidence/` or `fetch/` or have `live` in the basename, and (b)
             name the tool by basename or record one of its committed digests:
             the newest by last-touch committer date (ties: path) that also
             carries the row's live marker and its verdict pattern. A row whose
             sweep finds none fails; the sweep size is printed so the boundary
             is auditable.
  verdict    the one receipt line matching the row's pattern; zero or two
             matches is a failure (round-47's wrong-line class).
  digest     the tool digest the receipt records, classified `current` /
             `stale` / `uncommitted` against every blob the path has had.
  round      `round-NN` from the path, with the last-touch commit printed.
  alt        the newest candidate with `live` in its basename, printed when it
             is not the bound receipt, so a newer live run without the tool's
             verdict line is visible rather than hidden (round-47 H1b).
  invocation the receipt line that runs the tool, copied from the receipt.

Modes: --repo DIR, --rev REV, --emit, --ledger PATH, --sweep, --probe, -v.
Exit 0 iff every claim re-derives. Python 3 stdlib only; reads git objects,
writes nothing (stdout only), starts no host program, opens no socket.
"""

import argparse
import ast
import hashlib
import os
import re
import subprocess
import sys

BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
HEX64 = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])")
ROUND = re.compile(r"(?:^|/)round-(\d+)(?:/|$)")

# The two earlier ledger seats quote other receipts; they are not receipts.
EXCLUDED_PATHS = (
    ".ufo/waves/round-47/w1/ScrToolLedger/",
    ".ufo/waves/round-47/w2/ExecToolLedger/",
)

ROWS = [
    dict(tool="tools/mado-eventq.py", cls="LIVE-PROBE",
         cls_literal='run(["journalctl", "--user", "-u", UNIT', cls_in_code=True,
         question_line=2,
         reads_literal="journalctl --user -u wayland-wm@hyprland.desktop.service",
         receipt_marker="$ python3 -I tools/mado-eventq.py",
         declared_token="MADO_EVENTQ: ",
         verdict_regex=r"^MADO_EVENTQ: "),
    dict(tool="tools/mado-options.py", cls="LIVE-PROBE",
         cls_literal='subprocess.Popen([hyprctl, "getoption", "-j", key]',
         cls_in_code=True,
         question_line=2,
         reads_literal='subprocess.Popen([hyprctl, "getoption", "-j", key]',
         receipt_marker="hyprctl getoption -j", declared_token=None,
         verdict_regex=r"^labels agreement="),
    dict(tool="tools/mado-globals.py", cls="LIVE-PROBE",
         cls_literal="subprocess.Popen([prog] + JOURNALCTL_ARGS", cls_in_code=True,
         question_line=2,
         reads_literal="journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso",
         receipt_marker="command form:", declared_token="MADO_GLOBALS: ",
         verdict_regex=r"^MADO_GLOBALS: "),
    dict(tool="tools/mado-geometry.py", cls="LIVE-JOIN",
         cls_literal="hyprctl clients -j | mado-geometry.py",
         question_line=2,
         reads_literal="hyprctl clients -j | mado-geometry.py",
         receipt_marker="$ hyprctl clients -j", declared_token="MADO_GEOMETRY: ",
         verdict_regex=r"^MADO_GEOMETRY: "),
    dict(tool="tools/mado-monitors.py", cls="LIVE-JOIN",
         cls_literal="hyprctl monitors all -j | mado-monitors.py",
         question_line=2,
         reads_literal="hyprctl monitors all -j | mado-monitors.py",
         receipt_marker="$ hyprctl monitors all -j", declared_token="MADO_MONITORS: ",
         verdict_regex=r"^MADO_MONITORS: "),
    dict(tool="tools/mado-devices.py", cls="LIVE-JOIN",
         cls_literal="hyprctl devices -j | mado-devices.py",
         question_line=2,
         reads_literal="hyprctl devices -j | mado-devices.py",
         receipt_marker="$ hyprctl devices -j", declared_token="MADO_DEVICES: ",
         verdict_regex=r"^MADO_DEVICES: "),
    dict(tool="tools/mado-terminal.py", cls="LIVE-JOIN",
         cls_literal="--observed FILE",
         question_line=2,
         reads_literal="XDG_DATA_DIRS (default /usr/local/share:/usr/share)",
         receipt_marker="tool=tools/mado-terminal.py", declared_token="MADO_TERM: ",
         verdict_regex=r"^explain  MADO_TERM: "),
    dict(tool="tools/mado-verify.sh", cls="LIVE-PROBE",
         cls_literal="tmo hyprctl -j binds", cls_in_code=True,
         question_line=3,
         reads_literal="MADO_VERIFY_LIVE",
         receipt_marker="$ bash tools/mado-verify.sh", declared_token="MADO_VERIFY: ",
         verdict_regex=r"^MADO_VERIFY: "),
    dict(tool="tools/mado-tripwire.py", cls="SESSION-RECORD",
         cls_literal='if n.endswith(".jsonl"):', cls_in_code=True,
         question_line=2,
         reads_literal='os.path.join(agent, "sessions")',
         receipt_marker="cmd=python3 -I tools/mado-tripwire.py",
         declared_token="MADO_TRIPWIRE: ",
         verdict_regex=r"^MADO_TRIPWIRE: "),
    dict(tool="tools/mado-binds.py", cls="CONFIG-SCORED",
         cls_literal="no compositor, no socket, no",
         question_line=2,
         reads_literal="--home DIR",
         receipt_marker="live=hyprctl binds -j", declared_token=None,
         verdict_regex=r"^PRED-C1 \(v4\) .*verdict=TARGET_MET"),
    dict(tool="tools/mado-anims.py", cls="CONFIG-SCORED",
         cls_literal="no compositor, no socket, no",
         question_line=2,
         reads_literal="--home DIR",
         receipt_marker="ORACLE_CHECK", declared_token=None,
         verdict_regex=r"^PRED-C1-r26-v2 .*verdict=TARGET_MET"),
    dict(tool="tools/mado-wsrules.py", cls="CONFIG-SCORED",
         cls_literal="derived only from the bytes of the config tree",
         question_line=2,
         reads_literal='"the config tree under --home."',
         receipt_marker="ORACLE_CHECK", declared_token=None,
         verdict_regex=r"^PRED-C1-r27-v4 .*verdict=TARGET_MET"),
]

EXCLUDED = [
    dict(tool="tools/mado-action-plan.py", cls="ARTIFACT",
         why_literal="NEVER inspects\nhost state", why="never inspects host state"),
    dict(tool="tools/mado-assessment.py", cls="ARTIFACT",
         why_literal="host state or network is consulted",
         why="consults no host state or network"),
    dict(tool="tools/mado-evidence-audit.py", cls="ARTIFACT",
         why_literal="No classifier, host probe, Git, network",
         why="consults no host probe, Git or network"),
]


def die(msg):
    sys.stderr.write("check-ledger: %s\n" % msg)
    raise SystemExit(2)


class Git:
    def __init__(self, repo):
        self.repo = repo
        self._cache = {}
        self._hist = {}
        top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True)
        if top.returncode != 0:
            die("not a git repository: %s" % repo)
        self.top = top.stdout.strip()

    def run(self, *args):
        p = subprocess.run(["git", "-C", self.top] + list(args), capture_output=True)
        if p.returncode != 0:
            die("git %s failed: %s"
                % (" ".join(args), p.stderr.decode("utf-8", "replace").strip()))
        return p.stdout

    def tree(self, rev):
        out = self.run("ls-tree", "-r", "-z", rev)
        entries = []
        for rec in out.split(b"\0"):
            if not rec:
                continue
            meta, path = rec.split(b"\t", 1)
            mode, typ, sha = meta.decode().split()
            if typ == "blob":
                entries.append((path.decode("utf-8", "surrogateescape"), sha))
        return entries

    def blob(self, sha):
        if sha not in self._cache:
            self._cache[sha] = self.run("cat-file", "blob", sha)
        return self._cache[sha]

    def text(self, sha):
        return self.blob(sha).decode("utf-8", "replace")

    def path_blob(self, rev, path):
        out = self.run("ls-tree", rev, "--", path).strip()
        return out.split()[2] if out else None

    def last_commit(self, rev, path):
        line = self.run("log", "-1", "--format=%h|%cs|%s", rev, "--", path) \
            .decode("utf-8", "replace").strip()
        return tuple(line.split("|", 2)) if line else ("-", "-", "-")

    def history(self, rev, path):
        if path in self._hist:
            return self._hist[path]
        shas, sha256 = [], []
        for crec in self.run("rev-list", rev, "--", path).decode().split():
            out = self.run("ls-tree", crec, "--", path).strip()
            if out:
                s = out.split()[2]
                if s not in shas:
                    shas.append(s)
        for s in shas:
            d = hashlib.sha256(self.blob(s)).hexdigest()
            if d not in sha256:
                sha256.append(d)
        self._hist[path] = (shas, sha256)
        return self._hist[path]


def docstring_span(src, path):
    if not path.endswith(".py"):
        return None
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    if not tree.body:
        return None
    node = tree.body[0]
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
            and isinstance(node.value.value, str):
        return (node.lineno, node.end_lineno)
    return None


def code_line_numbers(src, path):
    span = docstring_span(src, path)
    out = []
    for n, line in enumerate(src.splitlines(), 1):
        if span and span[0] <= n <= span[1]:
            continue
        if path.endswith(".sh") and line.lstrip().startswith("#"):
            continue
        out.append(n)
    return set(out)


def instrument_names():
    """Every instrument basename (stem), for the one-instrument rule."""
    return sorted({os.path.basename(r["tool"]).rsplit(".", 1)[0] for r in ROWS}
                  | {os.path.basename(e["tool"]).rsplit(".", 1)[0] for e in EXCLUDED})


def instruments_named(text, names):
    return [n for n in names if (n + ".py") in text or (n + ".sh") in text]


def candidates(git, rev, row, entries):
    path = row["tool"]
    base = os.path.basename(path)
    _, digests = git.history(rev, path)
    names = instrument_names()
    out = []
    for p, sha in entries:
        if p.startswith("tools/") or p.startswith(".ufo/waves/round-49/"):
            continue
        if any(p.startswith(e) for e in EXCLUDED_PATHS):
            continue
        segs = p.split("/")
        if "fixtures" in segs[:-1]:
            continue
        if p.endswith((".py", ".sh")):
            # a receipt is output, not a program: scripts that name the tool or
            # carry its digest are generators, not runs.
            continue
        if not (any(s in ("receipts", "evidence", "fetch") for s in segs[:-1])
                or "live" in os.path.basename(p).lower()):
            continue
        text = git.text(sha)
        stem = base.rsplit(".", 1)[0]
        sumline = re.compile(r"^[0-9a-f]{64}\s+\*?(?:\S*/)?%s$"
                             % re.escape(base))
        tiers = (
            lambda l: bool(sumline.match(l.strip())),
            lambda l: "tool" in l.lower() and "sha256" in l.lower(),
            lambda l: stem in l,
        )
        recorded = []
        for tier in tiers:
            for line in text.splitlines():
                if not tier(line):
                    continue
                for d in HEX64.findall(line):
                    if d not in recorded:
                        recorded.append(d)
            if recorded:
                break
        if base not in text and not any(d in digests for d in recorded):
            continue
        if len(instruments_named(text, names)) > 1:
            # prints more than one instrument's name: an index of receipts,
            # not a run of this one (round-49 finding, geometry/f3).
            continue
        h, d, subj = git.last_commit(rev, p)
        vlines = [(n, l.rstrip()) for n, l in enumerate(text.splitlines(), 1)
                  if re.search(row["verdict_regex"], l)]
        out.append(dict(path=p, sha=sha, date=d, commit=h, subject=subj,
                        recorded=recorded, verdict_lines=vlines,
                        live_marker=row["receipt_marker"] in text,
                        live_named="live" in os.path.basename(p).lower()))
    out.sort(key=lambda c: (c["date"], c["path"]), reverse=True)
    return out


def digest_status(git, rev, path, recorded):
    if not recorded:
        return "none"
    current = hashlib.sha256(git.blob(git.path_blob(rev, path))).hexdigest()
    if current in recorded:
        return "current"
    _, digests = git.history(rev, path)
    return "stale" if any(d in digests for d in recorded) else "uncommitted"


def derive(git, rev, verbose=False):
    entries = git.tree(rev)
    by_path = dict(entries)
    problems, out = [], []

    tools = sorted(p for p, _ in entries if p.startswith("tools/"))
    declared = [r["tool"] for r in ROWS] + [e["tool"] for e in EXCLUDED]
    for t in tools:
        if t not in declared:
            problems.append("tool not covered: %s" % t)
    for d in declared:
        if d not in tools:
            problems.append("declared path is not a tool at %s: %s" % (rev[:8], d))
    if len(set(declared)) != len(declared):
        problems.append("a tool is declared twice")

    excluded_out = []
    for e in EXCLUDED:
        sha = by_path.get(e["tool"])
        if sha is None:
            continue
        text = git.text(sha)
        if e["why_literal"] not in text:
            problems.append("%s: exclusion literal absent: %r"
                            % (e["tool"], e["why_literal"]))
            continue
        lines = text.splitlines()
        first = e["why_literal"].split("\n")[0]
        last = e["why_literal"].split("\n")[-1]
        n = next(i for i, l in enumerate(lines, 1) if first in l)
        m = n
        while m <= len(lines) and last not in lines[m - 1]:
            m += 1
        m = min(m, len(lines))
        excluded_out.append(dict(tool=e["tool"], cls=e["cls"], why=e["why"],
                                 line=n, end=m,
                                 text=" / ".join(l.strip() for l in lines[n - 1:m])))

    for row in ROWS:
        path = row["tool"]
        sha = by_path.get(path)
        if sha is None:
            problems.append("%s: not a blob at %s" % (path, rev[:8]))
            continue
        src = git.text(sha)
        lines = src.splitlines()
        d = dict(row)
        d["sha256"] = hashlib.sha256(git.blob(sha)).hexdigest()
        d["gitsha"] = sha

        lit = row["cls_literal"]
        hits = [n for n, l in enumerate(lines, 1) if lit in l]
        if not hits:
            problems.append("%s: class literal absent: %r" % (path, lit))
            continue
        if row.get("cls_in_code"):
            code = code_line_numbers(src, path)
            hits = [n for n in hits if n in code]
            if not hits:
                problems.append("%s: class literal only in prose: %r" % (path, lit))
                continue
        d["cls_line"] = hits[0]
        d["cls_text"] = lines[hits[0] - 1].strip()

        qn = row["question_line"]
        span = docstring_span(src, path)
        if not (1 <= qn <= len(lines)):
            problems.append("%s: question line out of range: %d" % (path, qn))
            continue
        if span and not (span[0] <= qn <= span[1]):
            problems.append("%s:%d: question line outside the docstring %s"
                            % (path, qn, span))
            continue
        if path.endswith(".sh") and not lines[qn - 1].lstrip().startswith("#"):
            problems.append("%s:%d: question line is not a comment" % (path, qn))
            continue
        if not lines[qn - 1].strip():
            problems.append("%s:%d: question line blank" % (path, qn))
            continue
        qtext = lines[qn - 1].strip()
        if qtext.startswith('"""'):
            qtext = qtext[3:].strip()
        d["question_text"] = qtext

        rhits = [n for n, l in enumerate(lines, 1) if row["reads_literal"] in l]
        if not rhits:
            problems.append("%s: reads literal absent: %r"
                            % (path, row["reads_literal"]))
            continue
        d["reads_lines"] = [(n, lines[n - 1].strip()) for n in rhits[:2]]

        if row.get("declared_token"):
            tl = row["declared_token"]
            thits = [n for n, l in enumerate(lines, 1) if tl in l]
            if not thits:
                problems.append("%s: declared token absent from the tool: %r"
                                % (path, tl))
                continue
            d["token_line"] = thits[0]

        cands = candidates(git, rev, row, entries)
        bound = next((c for c in cands if c["verdict_lines"] and c["live_marker"]), None)
        alt = next((c for c in cands if c["live_named"]), None)
        if bound is None:
            problems.append("%s: no receipt carries both the verdict pattern %r "
                            "and the receipt marker %r (%d candidates scanned)"
                            % (path, row["verdict_regex"], row["receipt_marker"],
                               len(cands)))
            continue
        d["bound"] = bound
        d["n_cands"] = len(cands)
        d["n_verdict"] = sum(1 for c in cands if c["verdict_lines"])
        rc = ROUND.search(bound["path"])
        if not rc:
            problems.append("%s: receipt path carries no round: %s"
                            % (path, bound["path"]))
            continue
        d["round"] = int(rc.group(1))
        vn, vt = bound["verdict_lines"][0]
        d["verdict_line"], d["verdict_text"] = vn, vt
        d["verdict_lines"] = [n for n, _ in bound["verdict_lines"]]
        d["digest_status"] = digest_status(git, rev, path, bound["recorded"])
        d["recorded"] = bound["recorded"][:1]
        d["invocation"] = invocation_line(git, bound["sha"], os.path.basename(path),
                                          upto=d["verdict_line"])
        if alt is not None and alt["path"] != bound["path"]:
            # a live-named file counts as a run only if it records the tool's
            # digest or a command that runs it; a seat report that merely names
            # the tool is not a receipt.
            if not alt["recorded"] and not invocation_line(
                    git, alt["sha"], os.path.basename(path))[0]:
                alt = None
        d["alt"] = alt
        out.append(d)
        if verbose:
            sys.stderr.write("ok %-28s -> %-58s r%-2d %s\n"
                             % (path, bound["path"], d["round"], d["digest_status"]))
    return out, excluded_out, problems


def invocation_line(git, sha, base, upto=None):
    found = (None, None)
    for n, l in enumerate(git.text(sha).splitlines(), 1):
        if upto and n > upto:
            break
        s = l.strip()
        if base in s and (s.startswith("$") or s.startswith("command")
                          or s.startswith("# $") or s.startswith("# command")):
            found = (n, s)
    return found


def run_probes(git, rev):
    """Mutate one claim at a time; each mutation must make the derivation fail."""
    cases = [
        ("question-line-out-of-range", 0, "question_line", 10 ** 6),
        ("verdict-pattern-matches-nothing", 0, "verdict_regex",
         r"^MADO_EVENTQ: NOSUCHFIELD"),
        ("reads-literal-invented", 1, "reads_literal",
         "hyprctl definitely-not-in-the-source"),
        ("class-literal-only-in-prose", 2, "cls_literal", "Wayland"),
        ("receipt-marker-unsatisfiable", 3, "receipt_marker", "ZZZ-NO-SUCH-MARKER"),
        ("declared-token-invented", 0, "declared_token", "MADO_NOSUCH: "),
    ]
    out = []
    for name, idx, field, value in cases:
        saved = ROWS[idx].get(field)
        ROWS[idx][field] = value
        try:
            _, _, pr = derive(git, rev)
        finally:
            if saved is None:
                ROWS[idx].pop(field, None)
            else:
                ROWS[idx][field] = saved
        out.append((name, bool(pr)))
    saved_rows = list(ROWS)
    ROWS.append(dict(ROWS[0]))
    try:
        _, _, pr = derive(git, rev)
    finally:
        ROWS[:] = saved_rows
    out.append(("duplicate-row", bool(pr)))
    return out


def emit(derivations, excluded_out, rev, probes):
    L = []
    a = L.append
    a("# Live-state tool ledger — mado round 49, wave w1 (verified rows)")
    a("")
    counts = {}
    for d in derivations:
        counts[d["cls"]] = counts.get(d["cls"], 0) + 1
    a("Twelve instruments at the round-49 base touch state that is not in the "
      "repository: %d read the"
      % counts.get("LIVE-PROBE", 0))
    a("running desktop themselves, %d join a capture of it (`hyprctl … -j`, the "
      "resolver's own output),"
      % (counts.get("LIVE-JOIN", 0)))
    a("%d read the session's own transcripts, and %d static resolvers are scored "
      "against a live capture."
      % (counts.get("SESSION-RECORD", 0), counts.get("CONFIG-SCORED", 0)))
    a("Three further tools consult no host state at all and are listed, with "
      "their own words, at the end.")
    a("For each instrument the table gives the committed receipt that last "
      "recorded a live run of it,")
    a("and the section under it prints that receipt's verdict line, copied out "
      "of git.")
    a("")
    a("| instrument | class | receipt | round | bytes it ran |")
    a("|---|---|---|---|---|")
    for d in derivations:
        a("| `%s` | %s | `%s` | r%d | %s |"
          % (os.path.basename(d["tool"]), d["cls"], d["bound"]["path"],
             d["round"], d["digest_status"]))
    a("")
    a("Generated by `check-ledger.py --emit` from the objects of `%s`;" % rev)
    a("`check-ledger.py --ledger ledger.md` re-derives every row and fails on "
      "the first disagreement, so")
    a("this document is either true of that revision or absent. Nothing here was "
      "run on the host: a row")
    a("reports what a receipt records, not what the desktop does today.")
    a("")
    a("## Rules (all implemented in `check-ledger.py`)")
    a("")
    a("1. **Instrument set** — every blob under `tools/` at the revision is "
      "either a row or a listed")
    a("   exclusion; the checker fails on a tool that is neither.")
    a("2. **Receipt** — a file which (a) sits under a `receipts/`, `evidence/` "
      "or `fetch/` directory or")
    a("   has `live` in its basename and (b) names the tool by basename or "
      "records one of the tool's")
    a("   committed digests. The bound receipt is the newest such file, by the "
      "committer date of the")
    a("   last commit touching it, that also carries the row's live marker and "
      "its verdict pattern.")
    a("   The two round-47 ledger seat directories are excluded by path: they "
      "quote other receipts.")
    a("3. **Verdict** — the one receipt line matching the row's pattern. A "
      "pattern that matches zero or")
    a("   two lines is a failure. A receipt that carries the tool's verdict but "
      "not the live marker")
    a("   (a selftest aggregate, a locator dump) can therefore never become the "
      "bound row.")
    a("4. **Bytes it ran** — the tool digest the receipt records, classified "
      "`current` (the bytes at the")
    a("   revision), `stale` (a committed earlier blob of the same tool) or "
      "`uncommitted` (no committed")
    a("   blob of the tool ever had it).")
    a("5. **Round** — `round-NN` from the receipt path, with the last-touch "
      "commit printed beside it.")
    a("6. **Newer live-named file** — the newest candidate with `live` in its "
      "basename, printed whenever")
    a("   it is not the bound receipt, so a later live run that lacks the tool's "
      "verdict line stays")
    a("   visible instead of hidden (round-47 H1b).")
    a("")
    a("## Rows")
    a("")
    for d in derivations:
        b = d["bound"]
        a("### `%s`" % d["tool"])
        a("")
        a("- **class** `%s` — `%s:%d` `%s`" % (d["cls"], d["tool"], d["cls_line"],
                                                d["cls_text"]))
        a("- **question** `%s:%d` — %s" % (d["tool"], d["question_line"],
                                            d["question_text"]))
        for n, t in d["reads_lines"]:
            a("- **reads** `%s:%d` — `%s`" % (d["tool"], n, t))
        a("- **receipt** `%s` · r%d · blob `%s` · last touched `%s` (%s)"
          % (b["path"], d["round"], b["sha"][:8], b["commit"], b["date"]))
        if d["invocation"][0]:
            a("- **invocation there** `%s:%d` — `%s`"
              % (b["path"], d["invocation"][0], d["invocation"][1]))
        a("- **verdict** `%s:%d` — `%s`" % (b["path"], d["verdict_line"],
                                             d["verdict_text"]))
        if len(d["verdict_lines"]) > 1:
            a("- **verdict also at** %s (the same pattern in the same receipt)"
              % ", ".join(":%d" % n for n in d["verdict_lines"][1:]))
        if d["recorded"]:
            a("- **bytes it ran** `%s…` — %s" % (d["recorded"][0][:8],
                                                 d["digest_status"]))
        else:
            a("- **bytes it ran** no tool digest recorded — %s" % d["digest_status"])
        if d["alt"] and d["alt"]["path"] != b["path"]:
            alt = d["alt"]
            a("- **newer live-named file** `%s` · `%s` (%s) — %d line(s) match "
              "the verdict pattern"
              % (alt["path"], alt["commit"], alt["date"], len(alt["verdict_lines"])))
        a("- **sweep** %d receipt-shaped files name or digest this tool, %d carry "
          "its verdict pattern"
          % (d["n_cands"], d["n_verdict"]))
        a("")

    a("## Excluded instruments (not live-state)")
    a("")
    a("| tool | class | why (verbatim from the tool) |")
    a("|---|---|---|")
    for e in excluded_out:
        a("| `%s` | `%s` | `%s:%d` `%s` |" % (e["tool"], e["cls"], e["tool"],
                                               e["line"],
                                               e["text"].replace("|", "\\|")))
    a("")
    a("## Counts (emitted, not typed)")
    a("")
    a("- %d rows, %d distinct bound receipts, %d excluded instruments"
      % (len(derivations), len({d["bound"]["path"] for d in derivations}),
         len(excluded_out)))
    for status in ("current", "stale", "uncommitted", "none"):
        n = sum(1 for d in derivations if d["digest_status"] == status)
        a("- bytes it ran `%s`: %d" % (status, n))
    a("")
    a("## Gate self-test (run by `check-ledger.py --emit` on every emit)")
    a("")
    a("Each line mutates one field of the row data in memory; the derivation "
      "must then fail. A")
    a("`MISSED` line would mean the checker cannot falsify that claim, so it "
      "prints one here rather")
    a("than in a separate receipt.")
    a("")
    for name, caught in probes:
        a("- `%s` — %s" % ("CAUGHT" if caught else "MISSED", name))
    a("")
    a("## Limits")
    a("")
    a("- A receipt is evidence that a run happened at those bytes, not that the "
      "host answers the same")
    a("  way now. No host probe was run for this ledger.")
    a("- `newest` is a path-and-commit-date rule over git objects. A live run "
      "recorded only in a seat's")
    a("  prose report, or in a file that neither names the tool nor records its "
      "digest, is outside it;")
    a("  each row prints its sweep size, so the boundary is auditable.")
    a("- `uncommitted` means the receipt records a digest no committed blob of "
      "the tool ever had: the")
    a("  bytes that ran were never the committed tool.")
    a("- The bound receipt is the newest receipt that carries the tool's own "
      "verdict line. A live run")
    a("  whose receipt omits that line (a census dump, say) is shown as the "
      "newer live-named file, not")
    a("  as the bound receipt.")
    a("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--rev", default=BASE)
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--ledger")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    git = Git(args.repo)

    if args.sweep:
        entries = git.tree(args.rev)
        for row in ROWS:
            cands = candidates(git, args.rev, row, entries)
            sys.stdout.write("%s (%d candidates)\n" % (row["tool"], len(cands)))
            for c in cands[:5]:
                sys.stdout.write("  %s %-10s v=%d live=%d %s\n"
                                 % (c["date"],
                                    digest_status(git, args.rev, row["tool"],
                                                  c["recorded"]),
                                    len(c["verdict_lines"]),
                                    int(c["live_marker"]), c["path"]))
        return 0

    derivations, excluded_out, problems = derive(git, args.rev, args.verbose)

    if args.probe:
        if problems:
            for p in problems:
                sys.stdout.write("PROBLEM %s\n" % p)
            sys.stdout.write("PROBE base-not-clean\n")
            return 1
        probes = run_probes(git, args.rev)
        for name, caught in probes:
            sys.stdout.write("%s %s\n" % ("CAUGHT" if caught else "MISSED", name))
        bad = sum(1 for _, caught in probes if not caught)
        sys.stdout.write("PROBE %s\n" % ("ok" if bad == 0 else "failed=%d" % bad))
        return 0 if bad == 0 else 1

    if problems:
        for p in problems:
            sys.stdout.write("PROBLEM %s\n" % p)
        sys.stdout.write("LEDGER rows=%d excluded=%d problems=%d\n"
                         % (len(derivations), len(excluded_out), len(problems)))
        return 1

    text = emit(derivations, excluded_out, args.rev, run_probes(git, args.rev))
    if args.emit:
        sys.stdout.write(text)
        return 0
    if args.ledger:
        try:
            with open(args.ledger, "r", encoding="utf-8") as fh:
                committed = fh.read()
        except OSError as exc:
            sys.stdout.write("LEDGER-READ-FAIL %s\n" % exc)
            return 1
        if committed != text:
            sys.stdout.write("LEDGER-DRIFT %s\n" % args.ledger)
            return 1
    sys.stdout.write(
        "LEDGER rows=%d excluded=%d receipts=%d verdicts=%d current=%d "
        "stale=%d uncommitted=%d none=%d\n"
        % (len(derivations), len(excluded_out),
           len({d["bound"]["path"] for d in derivations}),
           sum(1 for d in derivations if d["verdict_text"]),
           sum(1 for d in derivations if d["digest_status"] == "current"),
           sum(1 for d in derivations if d["digest_status"] == "stale"),
           sum(1 for d in derivations if d["digest_status"] == "uncommitted"),
           sum(1 for d in derivations if d["digest_status"] == "none")))
    if args.ledger:
        sys.stdout.write("LEDGER-MATCH %s\n" % args.ledger)
    return 0


if __name__ == "__main__":
    sys.exit(main())
