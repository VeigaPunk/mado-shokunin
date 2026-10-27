#!/usr/bin/env python3
"""Mutant builder for the MutC1Counter seat (round 48 w2, FALSIFY).

One documented mutation per C1 clause (a/s/f/w/x/g/i/r) of the frozen counter
quality/counters/c1-r48-terminal-cache.py, plus one-rule probes derived from the data
candidate (.ufo/waves/round-48/l1-draft/mado-terminal.py) for the clauses the frozen
control corpus has no attacker for. Every anchor is asserted to occur exactly once.
Nothing in the lane is touched; output goes under the seat scratch root only.
"""
import difflib
import hashlib
import os
import sys

S = "/fast/scratch/hyaku/mado-r48/MutC1Counter"
L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(L, "quality/counters/c1-r48-terminal-cache.py")
TOOL = os.path.join(L, ".ufo/waves/round-48/l1-draft/mado-terminal.py")
OUT_MUT = os.path.join(S, "mut")
OUT_TOOL = os.path.join(S, "tool")

# (name, clause, description, [(old, new), ...])
COUNTER_MUTANTS = [
    ("a-revision-addressing-dropped", "a",
     "clause a: the tool is looked up in the worktree instead of the scored revision",
     [('    lane = lane_root()\n'
       '    ls = git(repo, "ls-tree", full, "--", TOOL)\n'
       '    present = bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"\n',
       '    lane = lane_root()\n'
       '    present = os.path.isfile(os.path.join(lane, TOOL))\n'),
      ('        with open(tool, "wb") as fh:\n'
       '            fh.write(git(repo, "show", "%s:%s" % (full, TOOL)))\n',
       '        with open(tool, "wb") as fh:\n'
       '            fh.write(open(os.path.join(lane, TOOL), "rb").read())\n')]),
    ("s-selftest-accepted", "s",
     "clause s: selftest accepted unconditionally (rc, N and the last line no longer checked)",
     [('    print("%s clause=s rc=%d last=%r" % (PRED, rc, last[:120]))\n'
       '    return "ok" if ok else "fail"\n',
       '    print("%s clause=s rc=%d last=%r" % (PRED, rc, last[:120]))\n'
       '    return "ok"\n')]),
    ("f-cold-accepted", "f",
     "clause f: every cold fixture accepted (the r47 harm-watch clause stops comparing)",
     [('            ok = ok_a and ok_b\n'
       '            f_ok += ok\n',
       '            ok = True\n'
       '            f_ok += ok\n')]),
    ("w-always-accept-warm", "w",
     "clause w: always-accept warm (comparison and class premise both dropped)",
     [('            check_premise(fx, st_a, cold_a)\n'
       '            ok = ok_a and ok_b\n'
       '            w_ok += ok\n',
       '            ok = True\n'
       '            w_ok += ok\n')]),
    ("x-observed-command-ignored", "x",
     "clause x: the two-item --observed capture dropped (a tool that ignores the command line is not caught)",
     [('    caps = ((0, o_norm, "AGREE", 0),\n'
       '            (1, o_norm.replace(".desktop", ".desktoq", 1), "DIFFER", 1),\n'
       '            (2, two, "DIFFER", 1))\n',
       '    caps = ((0, o_norm, "AGREE", 0),\n'
       '            (1, o_norm.replace(".desktop", ".desktoq", 1), "DIFFER", 1))\n')]),
    ("g-generated-accepted", "g",
     "clause g: every generated case accepted (both draws)",
     [('            ok, _o, why, _st, _c = run_case(box, case, "A", grng)\n'
       '            g_ok += ok\n',
       '            ok, _o, why, _st, _c = run_case(box, case, "A", grng)\n'
       '            g_ok += 1\n'),
      ('            ok, _o, why, st, cold = run_case(box, case, "A", grng)\n'
       '            check_premise(case, st, cold)\n'
       '            g_ok += ok\n',
       '            ok, _o, why, st, cold = run_case(box, case, "A", grng)\n'
       '            check_premise(case, st, cold)\n'
       '            g_ok += 1\n')]),
    ("i-no-write-tripwire", "i",
     "clause i / the no-write guard: the tool tree's .rw is writable for tool runs",
     [('        mode = "--ro-bind" if tool else "--bind"\n',
       '        mode = "--bind"\n')]),
    ("i-host-etc-bound", "i",
     "clause i: host /etc bound into the TOOL sandbox only (mount set no longer the enumerated one)",
     [('        if tool:\n'
       '            a += ["--ro-bind", self.python, "/usr/bin/python3", "--ro-bind", self.tool, "/oracle/tool.py"]\n',
       '        if tool:\n'
       '            a += ["--ro-bind", self.python, "/usr/bin/python3", "--ro-bind", self.tool, "/oracle/tool.py",\n'
       '                  "--ro-bind", "/etc", "/etc"]\n')]),
    ("r-no-tripwire", "r",
     "clause r: readonly is ok whatever the trace saw",
     [('        readonly = "fail" if box.trips else "ok"\n',
       '        readonly = "ok"\n')]),
]

# (name, targets, description, [(old, new), ...])  -- tool probes (one rule each)
TOOL_PROBES = [
    ("probe-selftest-rc", "s",
     "probe: the selftest prints N/N passed but exits 1 (clause s rc arm)",
     [('    return 0 if passed == total else 1\n', '    return 1\n')]),
    ("probe-x-observed-prefix", "x",
     "probe: explain --observed accepts a prefix of its own capture (ignores the command line)",
     [('        verdict = "AGREE" if mine == observed else "DIFFER"\n',
       '        verdict = "AGREE" if mine == observed or mine.startswith(observed) else "DIFFER"\n')]),
    ("probe-w-hit-content", "w",
     "probe: --print-content on a cache HIT reads a wrong path (warm answer only)",
     [('        try:\n'
       '            text = read_file(r.entry_path)\n',
       '        try:\n'
       '            text = read_file(r.entry_path + ".probe-hit" if getattr(r, "cache", "") == "hit"\n'
       '                             else r.entry_path)\n')]),
]


def read(p):
    with open(p, "rb") as fh:
        return fh.read().decode("utf-8", "surrogateescape")


def patch(text, pairs, name):
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            raise SystemExit("%s: anchor occurs %d times, not 1: %r" % (name, n, old[:90]))
        text = text.replace(old, new)
    return text


def emit(outdir, name, base_path, pairs, clause, desc, diffs):
    src = read(base_path)
    out = patch(src, pairs, name)
    with open(os.path.join(outdir, name + ".py"), "w", encoding="utf-8") as fh:
        fh.write(out)
    diff = "".join(difflib.unified_diff(src.splitlines(True), out.splitlines(True),
                                        os.path.basename(base_path), name + ".py", n=3))
    diffs.append("== %s [clause %s] %s\nbase %s sha256 %s\n%s\n" % (
        name, clause, desc, os.path.basename(base_path), hashlib.sha256(src.encode()).hexdigest(), diff))
    return name


def main():
    os.makedirs(OUT_MUT, exist_ok=True)
    os.makedirs(OUT_TOOL, exist_ok=True)
    os.makedirs(os.path.join(S, "out"), exist_ok=True)
    diffs = []
    for name, clause, desc, pairs in COUNTER_MUTANTS:
        emit(OUT_MUT, name, COUNTER, pairs, clause, desc, diffs)
    for name, clause, desc, pairs in TOOL_PROBES:
        emit(OUT_TOOL, name, TOOL, pairs, clause, desc, diffs)
    with open(os.path.join(S, "out", "patches.txt"), "w", encoding="utf-8") as fh:
        fh.write("".join(diffs))
    for d in (OUT_MUT, OUT_TOOL):
        for f in sorted(os.listdir(d)):
            if f.endswith(".py"):
                p = os.path.join(d, f)
                print("%s %s" % (hashlib.sha256(open(p, "rb").read()).hexdigest(), p))
    print("counter base sha256", hashlib.sha256(open(COUNTER, "rb").read()).hexdigest())
    print("tool base sha256", hashlib.sha256(open(TOOL, "rb").read()).hexdigest())


if __name__ == "__main__":
    sys.exit(main())
