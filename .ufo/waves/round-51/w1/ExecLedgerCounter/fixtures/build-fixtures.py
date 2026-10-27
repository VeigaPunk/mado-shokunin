#!/usr/bin/env python3
"""Build the C1 counter fixtures and print the measurement transcripts.

Round-51 w1, seat ExecLedgerCounter. Two things are measured with the same command line:

``base``  the lane at the frozen round base (no `quality/tool-ledger.md` at all) — must print
          `verdict=TARGET_MISSED ledger=absent` and exit 1.
``fx``    a synthetic git repository (population 5: `tools/alpha-tool.py`, `tools/beta.sh`,
          `quality/check-alpha.py`, `quality/check-tool-ledger.py`, `quality/counters/gamma.py`)
          with a complete ledger at its first commit — must print the frozen MET line and exit 0,
          and every one-row mutant after it must MISS on exactly the field it breaks.

The fixture repository carries a stand-in checker (`quality/check-tool-ledger.py` inside the
fixture only, never integrated) with the same row grammar and population rule, so the counter can
be exercised end to end without the lane's real checker.

Everything is written under `--scratch` (default: `$TMPDIR`), never to the lane, never to a
hard-coded temporary path. Nothing outside the scratch tree is touched.

Usage:
  python3 build-fixtures.py [--scratch DIR] [--counter PATH] [--repo LANE] [--base REV]
"""

import argparse
import os
import shutil
import subprocess
import sys

BASE_DEFAULT = "6ca8c559a4a3d6d361101592116eea2bc7452437"
STANDIN = r'''#!/usr/bin/env python3
"""Stand-in for quality/check-tool-ledger.py (fixture double: exercised, never integrated)."""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

LEDGER = "quality/tool-ledger.md"
PLACEHOLDER = re.compile(r"^[\s\-–—_*`.]+$")


def git(repo, *args):
    proc = subprocess.run(("git", "-C", repo) + args, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", "replace"))
        raise SystemExit(2)
    return proc.stdout


def files(repo, rev):
    return set(p for p in git(repo, "ls-tree", "-r", "--name-only", rev).decode().splitlines()
               if p)


def population(paths):
    out = []
    for path in paths:
        if "__pycache__" in path or path.endswith((".pyc", ".pyo")):
            continue
        if path.startswith("tools/"):
            out.append(path)
            continue
        for root in ("quality/counters/", "quality/"):
            if path.startswith(root):
                rest = path[len(root):]
                if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                    out.append(path)
                break
    return sorted(set(out))


def rows(text):
    out = []
    fenced = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = cells[0].strip("`*_ \t") if cells else ""
        if not first or "/" not in first or set(first) <= set("-: "):
            continue
        out.append((first, cells[1] if len(cells) > 1 else "",
                    " | ".join(cells[2:]) if len(cells) > 2 else ""))
    return out


def tokens(cell):
    found = re.findall(r"`([^`\n]+)`", cell)
    if not found:
        found = re.split(r"[,;]\s*", cell)
    out = []
    for token in found:
        token = re.sub(r":\d+(?:-\d+)?$", "", token.strip("`*_ \t"))
        if token and ("/" in token or re.search(r"\.(md|py|sh)$", token)):
            out.append(token)
    return out


def measure(repo, rev):
    present = files(repo, rev)
    pop = population(present)
    if LEDGER not in present:
        return dict(population=len(pop), ledger_rows=0, uncovered=len(pop), dangling=0,
                    bad_pointer=0, empty_desc=0), True
    ledger_rows = rows(git(repo, "show", "%s:%s" % (rev, LEDGER)).decode("utf-8", "replace"))
    popset, seen = set(pop), set()
    dangling = bad = empty = 0
    for path, desc, pointer in ledger_rows:
        if path not in popset:
            dangling += 1
            continue
        seen.add(path)
        clean = desc.strip("`*_ \t")
        if not clean or PLACEHOLDER.match(clean):
            empty += 1
        base = os.path.basename(path).encode()
        good = False
        for token in tokens(pointer):
            if token in present and base in git(repo, "show", "%s:%s" % (rev, token)):
                good = True
                break
        if not good:
            bad += 1
    return dict(population=len(pop), ledger_rows=len(ledger_rows),
                uncovered=len(popset - seen), dangling=dangling, bad_pointer=bad,
                empty_desc=empty), False


def summary(fields, rev):
    return ("LEDGER: population=%d ledger_rows=%d uncovered=%d dangling=%d bad_pointer=%d "
            "empty_desc=%d" % (fields["population"], fields["ledger_rows"],
                               fields["uncovered"], fields["dangling"],
                               fields["bad_pointer"], fields["empty_desc"]))


def selftest(work):
    root = tempfile.mkdtemp(prefix="selftest-", dir=work)
    repo = os.path.join(root, "repo")
    os.makedirs(os.path.join(repo, "tools"))
    os.makedirs(os.path.join(repo, "docs"))
    os.makedirs(os.path.join(repo, "quality"))
    def put(rel, text):
        full = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as handle:
            handle.write(text)
    def commit():
        git(repo, "add", "-A")
        git(repo, "-c", "user.name=fx", "-c", "user.email=fx@local", "commit", "-q", "-m", "x")
        return git(repo, "rev-parse", "HEAD").decode().strip()
    git(repo, "init", "-q")
    put("tools/one.py", "x\n")
    put("docs/inv.md", "names one.py\n")
    put("quality/tool-ledger.md",
        "| file | description | pointer |\n|---|---|---|\n"
        "| `tools/one.py` | the one tool | `docs/inv.md` |\n")
    good = commit()
    put("quality/tool-ledger.md", "| file | description | pointer |\n|---|---|---|\n")
    empty = commit()
    cases, results = 0, 0
    for rev, expect in ((good, "clean"), (empty, "uncovered")):
        fields, absent = measure(repo, rev)
        cases += 3
        results += 1 if not absent else 0
        results += 1 if (fields["uncovered"] == 0) == (expect == "clean") else 0
        results += 1 if (fields["dangling"] == 0) else 0
    shutil.rmtree(root, ignore_errors=True)
    print("LEDGER_SELFTEST: %d/%d passed" % (results, cases))
    return 0 if results == cases else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        work = args.work or os.environ.get("TMPDIR") or tempfile.mkdtemp()
        os.makedirs(work, exist_ok=True)
        return selftest(work)
    if not args.rev:
        sys.stderr.write("--rev required\n")
        return 2
    rev = git(args.repo, "rev-parse", args.rev + "^{commit}").decode().strip()
    fields, absent = measure(args.repo, rev)
    if absent:
        print("LEDGER: population=%d verdict=TARGET_MISSED ledger=absent rev=%s"
              % (fields["population"], rev))
        return 1
    print(summary(fields, rev))
    clean = (fields["population"] > 0 and fields["ledger_rows"] == fields["population"]
             and not any(fields[k] for k in ("uncovered", "dangling", "bad_pointer",
                                             "empty_desc")))
    print("%s verdict=%s rev=%s" % (summary(fields, rev),
                                    "TARGET_MET" if clean else "TARGET_MISSED", rev))
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
'''

PARROT = r'''#!/usr/bin/env python3
"""Parrot checker (fixture mutant): prints a clean-looking LEDGER line without reading anything."""
import sys

args = sys.argv[1:]
if "--selftest" in args:
    print("LEDGER_SELFTEST: 2/2 passed")
    raise SystemExit(0)
rev = args[args.index("--rev") + 1] if "--rev" in args else "unknown"
print("LEDGER: population=6 ledger_rows=5 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 "
      "verdict=TARGET_MET rev=%s" % rev)
'''

ROWS = {
    "alpha": "| `tools/alpha-tool.py` | fixture alpha tool, prints nothing | `docs/inventory.md` |",
    "beta": "| `tools/beta.sh` | fixture shell tool, exits 0 | `docs/inventory.md` |",
    "check": "| `quality/check-alpha.py` | fixture gate over alpha-tool output | `docs/inventory.md` |",
    "gamma": "| `quality/counters/gamma.py` | fixture counter over beta.sh | `docs/inventory.md` |",
    "checker": "| `quality/check-tool-ledger.py` | fixture ledger checker | `docs/inventory.md` |",
}
HEADER = "| file | description | accountability |\n|---|---|---|\n"


def ledger(*names):
    return HEADER + "\n".join(ROWS[n] for n in names) + "\n"


def run(args, cwd):
    proc = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return proc.returncode, proc.stdout, proc.stderr


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default=os.environ.get("TMPDIR"))
    ap.add_argument("--counter", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "c1-r51-ledger.py"))
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/mado-shokunin")
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args(argv)

    scratch = args.scratch or subprocess.run(
        [sys.executable, "-c", "import tempfile;print(tempfile.gettempdir())"],
        capture_output=True, text=True).stdout.strip()
    scratch = os.path.abspath(scratch)
    root = os.path.join(scratch, "fx")
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    work = os.path.join(scratch, "work")
    os.makedirs(work, exist_ok=True)

    # ---- the synthetic repository ------------------------------------------
    repo = os.path.join(root, "repo")
    os.makedirs(repo)
    git = lambda *a: subprocess.run(("git", "-C", repo) + a, capture_output=True, text=True,
                                    check=True)
    git("init", "-q")
    top = git("rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(repo), (top, repo)

    def put(rel, text, mode=None):
        full = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as handle:
            handle.write(text)
        if mode:
            os.chmod(full, mode)

    def commit(message):
        git("add", "-A")
        git("-c", "user.name=fixture", "-c", "user.email=fixture@mado.local",
            "commit", "-q", "-m", message)
        return git("rev-parse", "HEAD").stdout.strip()

    put("tools/alpha-tool.py", "#!/usr/bin/env python3\n\"\"\"alpha.\"\"\"\nprint('alpha')\n")
    put("tools/beta.sh", "#!/bin/sh\nexit 0\n", 0o755)
    put("quality/check-alpha.py", "#!/usr/bin/env python3\n\"\"\"alpha gate.\"\"\"\n")
    put("quality/counters/gamma.py", "#!/usr/bin/env python3\n\"\"\"gamma counter.\"\"\"\n")
    put("quality/check-tool-ledger.py", STANDIN, 0o755)
    put("docs/inventory.md",
        "# fixture inventory\n\n"
        "- `tools/alpha-tool.py` - alpha\n- `tools/beta.sh` - beta\n"
        "- `quality/check-alpha.py` - alpha gate\n- `quality/counters/gamma.py` - gamma\n"
        "- `quality/check-tool-ledger.py` - checker\n")

    revs = {}
    put("quality/tool-ledger.md", ledger("alpha", "beta", "check", "gamma", "checker"))
    revs["complete"] = commit("fx: complete ledger")
    put("quality/tool-ledger.md", ledger("alpha", "check", "gamma", "checker"))
    revs["uncovered"] = commit("fx: omit tools/beta.sh")
    put("quality/tool-ledger.md",
        ledger("alpha", "beta", "check", "gamma", "checker").replace(
            "| `tools/beta.sh` | fixture shell tool, exits 0 | `docs/inventory.md` |",
            "| `tools/beta.sh` | fixture shell tool, exits 0 | `docs/missing.md` |"))
    revs["bad_pointer"] = commit("fx: beta pointer names a file that never names beta.sh")
    put("quality/tool-ledger.md",
        ledger("alpha", "beta", "check", "gamma", "checker").replace(
            "| `tools/beta.sh` | fixture shell tool, exits 0 |", "| `tools/beta.sh` | - |"))
    revs["empty_desc"] = commit("fx: beta description is a dash")
    put("quality/tool-ledger.md",
        ledger("alpha", "beta", "check", "gamma", "checker")
        + "| `tools/ghost.py` | row for a file that is not in the population | `docs/inventory.md` |\n")
    revs["dangling"] = commit("fx: dangling row")
    put("quality/tool-ledger.md",
        ledger("alpha", "beta", "check", "gamma", "checker") + ROWS["alpha"] + "\n")
    revs["dup"] = commit("fx: duplicate row")
    put("quality/check-tool-ledger.py",
        STANDIN.replace('print("LEDGER_SELFTEST: %d/%d passed" % (results, cases))\n    return 0 if results == cases else 1',
                        'print("LEDGER_SELFTEST: 1/4 passed")\n    return 1'))
    put("quality/tool-ledger.md", ledger("alpha", "beta", "check", "gamma", "checker"))
    revs["selftest_fail"] = commit("fx: checker selftest fails")
    put("quality/check-tool-ledger.py", PARROT, 0o755)
    put("quality/tool-ledger.md", ledger("alpha", "check", "gamma", "checker"))
    revs["parrot"] = commit("fx: parrot checker over a ledger that omits tools/beta.sh")
    put("quality/tool-ledger.md", ledger("alpha", "beta", "check", "gamma", "checker"))
    revs["disagree"] = commit("fx: checker advertises a population the tree does not have")
    put("quality/check-tool-ledger.py", STANDIN, 0o755)
    put("quality/tool-ledger.md",
        ledger("alpha", "beta", "check", "gamma", "checker")
        + "\n```\n| `tools/ghost.py` | fenced grammar example | `docs/inventory.md` |\n```\n")
    revs["fenced"] = commit("fx: fenced example row must not become a ledger row")
    os.remove(os.path.join(repo, "quality/tool-ledger.md"))
    revs["absent"] = commit("fx: no ledger")

    # ---- transcripts --------------------------------------------------------
    out = []

    def emit(title, cmd):
        rc, stdout, stderr = run(cmd, cwd=work)
        out.append("$ %s\n%s%s-> exit %d\n" % (
            " ".join(cmd), stdout, ("[stderr] " + stderr) if stderr else "", rc))
        print("== %s -> exit %d" % (title, rc))
        print(stdout.strip())
        if stderr.strip():
            print("[stderr] " + stderr.strip())
        return rc

    print("scratch=%s" % scratch)
    print("counter=%s" % args.counter)
    emit("lane at base %s" % args.base[:12],
         [sys.executable, "-I", args.counter, "--repo", args.repo, "--rev", args.base,
          "--work", work, "--checker", "quality/check-tool-ledger.py"])
    emit("fixture complete ledger",
         [sys.executable, "-I", args.counter, "--repo", repo, "--rev", revs["complete"],
          "--work", work])
    for name in ("uncovered", "bad_pointer", "empty_desc", "dangling", "dup", "selftest_fail",
                 "parrot", "disagree"):
        emit("fixture mutant %s" % name,
             [sys.executable, "-I", args.counter, "--repo", repo, "--rev", revs[name],
              "--work", work])
    emit("fixture fenced example (documentation, must stay TARGET_MET)",
         [sys.executable, "-I", args.counter, "--repo", repo, "--rev", revs["fenced"],
          "--work", work])
    emit("fixture absent ledger",
         [sys.executable, "-I", args.counter, "--repo", repo, "--rev", revs["absent"],
          "--work", work])
    emit("setup error: bogus rev",
         [sys.executable, "-I", args.counter, "--repo", repo, "--rev", "deadbeef",
          "--work", work])

    print("\nrevs:")
    for name, rev in revs.items():
        print("  %-14s %s" % (name, rev))
    print("\n--- transcript ---")
    print("".join(out))
    leftovers = [p for p in os.listdir(work)]
    print("work leftovers after runs: %s" % (leftovers or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
