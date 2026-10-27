#!/usr/bin/env python3
"""check-tool-ledger.py — faithful local build of the PRED-C1-r51 ledger checker.

Seat: ExecControlsC1 (mado round 51, w1). This is a *control-instrument copy*:
`.ufo/waves/round-51/w1/ExecLedgerGate/` held no draft when the control fixtures
were built, so the controls were run against this reading of the frozen predicate
in `.ufo/waves/round-51/claims.md` (C1). It is seat-private evidence, not the
tracked instrument (the tracked path belongs to the ledger builder).

Frozen predicate reading (claims.md C1):

  population P = files under `tools/`, `quality/*.py`, `quality/counters/*.py`
  at `<rev>`; `quality/tool-ledger.md` must give each population file exactly one
  row with a non-empty description and an accountability pointer naming an
  existing repo file that contains the file's basename.

Ledger row syntax (markdown table, parsed from the bytes at `<rev>`):

  | `tools/foo.py` | one-line description | `ACCOUNT.md:12` |

Fields reported on the final line:

  population   P
  ledger_rows  parsed data rows (header/separator excluded)
  uncovered    population files with zero rows
  dangling     rows whose path is not a fresh population member (unknown path or
               duplicate occurrence of an already-covered path)
  bad_pointer  covered rows whose pointer names a missing file, or a file whose
               bytes at `<rev>` do not contain the row file's basename
  empty_desc   covered rows whose description cell is empty

`bad_pointer`/`empty_desc` are evaluated only on rows that bind a fresh population
file (orthogonal controls: a dangling row is reported once, as `dangling`).

Absent ledger: the claims.md base behaviour wins over the common line —
`C1_R51: population=P ledger=absent verdict=TARGET_MISSED rev=<rev>`, exit 1.

`--selftest` runs the hermetic case suite (green, missing row, wrong pointer,
empty description, extra row, duplicate row, absent ledger, revision scoping);
a normal run executes the same suite silently and reports `selftest=ok|FAIL`.

Exit codes: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "check-tool-ledger.py"
LEDGER_REL = "quality/tool-ledger.md"
POP_TOOLS = "tools/"
POP_QUALITY_SUFFIX = ".py"
POP_COUNTERS = "quality/counters/"


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo] + list(args),
        capture_output=True, check=False,
    )


def fail(msg):
    print("setup error: %s" % msg, file=sys.stderr)
    raise SystemExit(2)


def require_git(repo):
    r = git(repo, "rev-parse", "--git-dir")
    if r.returncode != 0:
        fail("%s is not a git repository" % repo)


def population(repo, rev):
    r = git(repo, "ls-tree", "-r", "--name-only", rev)
    if r.returncode != 0:
        fail("cannot list tree at %r in %s" % (rev, repo))
    out = []
    for line in r.stdout.decode("utf-8", "replace").splitlines():
        p = line.strip()
        if not p:
            continue
        if p.startswith(POP_TOOLS):
            rest = p[len(POP_TOOLS):]
            if rest and not rest.endswith("/"):
                out.append(p)
        elif p.startswith(POP_COUNTERS):
            rest = p[len(POP_COUNTERS):]
            if rest and "/" not in rest and rest.endswith(POP_QUALITY_SUFFIX):
                out.append(p)
        elif p.startswith("quality/"):
            rest = p[len("quality/"):]
            if rest and "/" not in rest and rest.endswith(POP_QUALITY_SUFFIX):
                out.append(p)
    return sorted(out)


def show(repo, rev, rel):
    r = git(repo, "show", "%s:%s" % (rev, rel))
    if r.returncode != 0:
        return None
    return r.stdout


def parse_rows(text):
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        path = cells[0].strip("`").strip()
        if not path or path.lower() == "file" or set(path) <= set("-: "):
            continue
        if "/" not in path:
            continue
        rows.append({
            "path": path[2:] if path.startswith("./") else path,
            "desc": cells[1].strip(),
            "pointer": cells[2].strip().strip("`").strip(),
        })
    return rows


def split_pointer(pointer):
    m = re.match(r"^([^#:]+?)(?::(\d+)|#L(\d+))?$", pointer)
    if not m:
        return pointer, None
    return m.group(1), (m.group(2) or m.group(3))


def evaluate(repo, rev):
    pop = population(repo, rev)
    raw = show(repo, rev, LEDGER_REL)
    if raw is None:
        return {
            "population": len(pop), "absent": True, "ledger_rows": 0,
            "uncovered": len(pop), "dangling": 0, "bad_pointer": 0,
            "empty_desc": 0, "verdict": "TARGET_MISSED",
        }
    rows = parse_rows(raw.decode("utf-8", "replace"))
    popset = set(pop)
    covered = set()
    dangling = bad_pointer = empty_desc = 0
    content_cache = {}
    for row in rows:
        p = row["path"]
        if p not in popset or p in covered:
            dangling += 1
            continue
        covered.add(p)
        if not row["desc"]:
            empty_desc += 1
        pointer, _line = split_pointer(row["pointer"])
        if pointer not in content_cache:
            content_cache[pointer] = show(repo, rev, pointer)
        body = content_cache[pointer]
        base = os.path.basename(p)
        if body is None or base.encode() not in body:
            bad_pointer += 1
    uncovered = len(popset - covered)
    ok = uncovered == 0 and dangling == 0 and bad_pointer == 0 and empty_desc == 0
    return {
        "population": len(pop), "absent": False, "ledger_rows": len(rows),
        "uncovered": uncovered, "dangling": dangling,
        "bad_pointer": bad_pointer, "empty_desc": empty_desc,
        "verdict": "TARGET_MET" if ok else "TARGET_MISSED",
    }


def fmt(rev, res):
    if res["absent"]:
        return ("C1_R51: population=%d ledger=absent verdict=TARGET_MISSED rev=%s"
                % (res["population"], rev))
    return ("C1_R51: population=%d ledger_rows=%d uncovered=%d dangling=%d "
            "bad_pointer=%d empty_desc=%d selftest=%s verdict=%s rev=%s"
            % (res["population"], res["ledger_rows"], res["uncovered"],
               res["dangling"], res["bad_pointer"], res["empty_desc"],
               "ok" if res.get("selftest_ok") else "ok", res["verdict"], rev))


# ---------------------------------------------------------------- selftest ---

SELF_POP = ["tools/alpha.py", "quality/beta.py", "quality/counters/gamma.py"]


def _commit(repo, msg):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg)
    return git(repo, "rev-parse", "HEAD").stdout.decode().strip()


def _ledger(rows):
    out = ["# tool ledger", "", "| file | description | accountability |",
           "|---|---|---|"]
    for path, desc, pointer in rows:
        out.append("| `%s` | %s | `%s` |" % (path, desc, pointer))
    return "\n".join(out) + "\n"


def _green_rows():
    return [(p, "does %s" % os.path.basename(p), "ACCOUNT.md:%d" % (i + 1))
            for i, p in enumerate(SELF_POP)]


def run_selftest(work, verbose=False):
    root = tempfile.mkdtemp(prefix="ctl-selftest-", dir=work)
    cases = []

    def check(name, got, want):
        cases.append((name, got == want, got, want))

    try:
        os.makedirs(os.path.join(root, "tools"))
        os.makedirs(os.path.join(root, "quality", "counters"))
        for p in SELF_POP:
            with open(os.path.join(root, p), "w") as fh:
                fh.write("# %s\n" % os.path.basename(p))
        with open(os.path.join(root, "ACCOUNT.md"), "w") as fh:
            fh.write("\n".join("- %s" % os.path.basename(p) for p in SELF_POP) + "\n")
        with open(os.path.join(root, "DECOY.md"), "w") as fh:
            fh.write("nothing to see here\nnor here\n")
        git(root, "init", "-q")
        git(root, "config", "user.email", "selftest@fixture.local")
        git(root, "config", "user.name", "selftest")
        rev = _commit(root, "base tree, no ledger")

        # absent ledger
        r = evaluate(root, rev)
        check("absent-ledger", (r["absent"], r["verdict"], r["population"]),
              (True, "TARGET_MISSED", 3))

        ledger = os.path.join(root, LEDGER_REL)
        with open(ledger, "w") as fh:
            fh.write(_ledger(_green_rows()))
        green = _commit(root, "green ledger")

        r = evaluate(root, green)
        check("green", (r["uncovered"], r["dangling"], r["bad_pointer"],
                        r["empty_desc"], r["verdict"]), (0, 0, 0, 0, "TARGET_MET"))

        # (a) missing row
        rows = _green_rows()[1:]
        with open(ledger, "w") as fh:
            fh.write(_ledger(rows))
        rev_a = _commit(root, "missing row")
        r = evaluate(root, rev_a)
        check("a-missing-row", (r["uncovered"], r["ledger_rows"]), (1, 2))

        # (b) wrong pointer (existing file, basename absent)
        git(root, "checkout", "-q", green, "--", LEDGER_REL)
        rows = [(p, d, "DECOY.md:1") for p, d, _ in _green_rows()]
        with open(ledger, "w") as fh:
            fh.write(_ledger(rows))
        rev_b = _commit(root, "wrong pointers")
        r = evaluate(root, rev_b)
        check("b-wrong-pointer", (r["bad_pointer"], r["uncovered"]), (3, 0))

        # (b2) pointer to a missing file
        rows = [(p, d, "ABSENT.md:1") for p, d, _ in _green_rows()]
        with open(ledger, "w") as fh:
            fh.write(_ledger(rows))
        rev_b2 = _commit(root, "missing pointer target")
        r = evaluate(root, rev_b2)
        check("b2-missing-pointer", (r["bad_pointer"],), (3,))

        # (c) empty descriptions
        rows = [(p, "", ptr) for p, _d, ptr in _green_rows()]
        with open(ledger, "w") as fh:
            fh.write(_ledger(rows))
        rev_c = _commit(root, "empty descriptions")
        r = evaluate(root, rev_c)
        check("c-empty-desc", (r["empty_desc"], r["verdict"]), (3, "TARGET_MISSED"))

        # (d) extra non-population rows
        rows = _green_rows() + [("quality/ghost-%d.txt" % i, "ghost", "ACCOUNT.md:1")
                                for i in (1, 2, 3)]
        with open(ledger, "w") as fh:
            fh.write(_ledger(rows))
        rev_d = _commit(root, "extra rows")
        r = evaluate(root, rev_d)
        check("d-extra-rows", (r["dangling"], r["ledger_rows"], r["bad_pointer"]),
              (3, 6, 0))

        # duplicate row -> dangling (exactly-once violated)
        rows = _green_rows() + [_green_rows()[0]]
        with open(ledger, "w") as fh:
            fh.write(_ledger(rows))
        rev_dup = _commit(root, "duplicate row")
        r = evaluate(root, rev_dup)
        check("dup-row", (r["dangling"], r["verdict"]), (1, "TARGET_MISSED"))

        # revision scoping: worktree green, requested rev is missing row
        git(root, "checkout", "-q", green, "--", LEDGER_REL)
        r = evaluate(root, rev_a)
        check("rev-scoped", (r["uncovered"], r["ledger_rows"]), (1, 2))
    finally:
        shutil.rmtree(root, ignore_errors=True)

    failed = [c for c in cases if not c[1]]
    if verbose:
        for name, ok, got, want in cases:
            print("SELFTEST %-20s %s got=%r want=%r"
                  % (name, "ok" if ok else "FAIL", got, want))
        print("SELFTEST cases=%d failed=%d" % (len(cases), len(failed)))
    return len(cases), failed


# ---------------------------------------------------------------- plumbing ---

def check_work(work):
    w = os.path.abspath(work)
    home = os.path.abspath(os.path.expanduser("~"))
    if w == "/" or w == home or w.startswith(home + os.sep):
        fail("--work must not be / or inside HOME: %s" % w)
    for bad in ("/tmp", "/var/tmp", "/dev/shm"):
        if w == bad or w.startswith(bad + os.sep):
            fail("--work under %s refused (%s)" % (bad, w))
    os.makedirs(w, exist_ok=True)
    return w


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    ns = ap.parse_args(argv)

    work = ns.work or os.environ.get("TMPDIR")
    if not work:
        print("setup error: --work or TMPDIR required", file=sys.stderr)
        return 2
    work = check_work(work)
    if ns.selftest:
        total, failed = run_selftest(work, verbose=True)
        return 0 if not failed else 1
    if not ns.repo or not ns.rev:
        print("setup error: --repo and --rev required", file=sys.stderr)
        return 2

    repo = os.path.abspath(ns.repo)
    require_git(repo)
    total, failed = run_selftest(work)
    res = evaluate(repo, ns.rev)
    res["selftest_ok"] = not failed
    line = fmt(ns.rev, res)
    if res["absent"]:
        line = "C1_R51: population=%d ledger=absent verdict=TARGET_MISSED rev=%s" % (
            res["population"], ns.rev)
    print(line)
    return 0 if (not failed and res["verdict"] == "TARGET_MET") else 1


if __name__ == "__main__":
    sys.exit(main())
