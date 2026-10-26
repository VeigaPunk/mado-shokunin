#!/usr/bin/env python3
"""MutC2V2: demonstrate the missing-control inputs for mutants the registered
battery (74 controls + forge + more) does not kill.

Each fixture is control P plus one weakening input. It is scored against the
PRISTINE v2 counter (expected: rejected, via the clause the tightening lives in)
and against the named mutant (expected: admitted => the input kills that mutant).
PINS are extended with the fixture's own receipt bytes via the controls runner's
own patched_counter helper, so the rejection/admission is decided by the clause
under test, not by the pin check.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

S = "/fast/scratch/hyaku/mado-r43/MutC2V2"
RUNNER = os.path.join(S, "run-c2-controls-v2.py")
PRISTINE = os.path.join(S, "pristine-counter.py")
WORK = os.path.join(S, "probe", "work")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
os.environ["TMPDIR"] = os.path.join(WORK, "tmp")
os.makedirs(os.environ["TMPDIR"], exist_ok=True)

spec = importlib.util.spec_from_file_location("ctl", RUNNER)
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)

P = ctl.admitted()
FETCH = ctl.FETCH
ENTRY, SRC, LES = ctl.ENTRY, ctl.SRC, ctl.LES


def rep(g, key, old, new, count=1):
    assert old in g[key], (key, old[:60])
    g[key] = g[key].replace(old, new, count)


def line_of_bytes(data, quote):
    """1-based line where the whitespace-collapsed quote starts (own bytes)."""
    flat, where, prev = [], [], True
    for ln, line in enumerate(data.decode("utf-8", "replace").split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    flat.append(" ")
                    where.append(ln)
                    prev = True
            else:
                flat.append(ch)
                where.append(ln)
                prev = False
    k = "".join(flat).find(quote)
    assert k >= 0
    return where[k]


def patched_counter_last(dest, files):
    """patched_counter variant that appends the fixture hashes AFTER the
    original PINS entries: for a basename in both, the fixture's (edited)
    bytes win. The frozen runner's patched_counter inserts them first, and a
    later duplicate dict key wins, so an edited pinned receipt can never
    satisfy pin_ok there."""
    src = open(ctl.COUNTER).read()
    extra = "".join('    "%s": "%s",\n' % (os.path.basename(k), ctl.sha(v))
                    for k, v in files.items()
                    if k.startswith(FETCH) and not isinstance(v, bool))
    anchor = ('    "Hyprland-WindowTarget.cpp": '
              '"8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d",\n}')
    assert anchor in src, "PINS anchor missing"
    src = src.replace(
        anchor,
        '    "Hyprland-WindowTarget.cpp": '
        '"8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d",\n'
        + extra + "}", 1)
    path = os.path.join(dest, "c2-patched-last.py")
    open(path, "w").write(src)
    return path


def score(counter, files):
    d = tempfile.mkdtemp(prefix="pr-", dir=WORK)
    try:
        ctl.COUNTER = counter
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ENV).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), (top, d)
        b = ctl.commit_all(d, ctl.base_files(), "base")
        a = ctl.commit_all(d, files, "after")
        c2 = patched_counter_last(tempfile.mkdtemp(prefix="pc-", dir=WORK), files)
        p = subprocess.run([sys.executable, "-I", c2, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        cls = [l for l in lines if " clauses=" in l]
        clauses = cls[0].split(" clauses=")[1].split(" admitted")[0] if cls else "-"
        last = lines[-1] if lines else "NO-OUTPUT " + p.stderr[-160:]
        return p.returncode, last.split(": ", 1)[-1].split(" rev=")[0], clauses
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------- fixtures
def fx_comment_py(g):
    """F-2b: GATE quote lives only inside a '#' comment of gkeep-ui-excerpt.py."""
    q = "the size request is ignored by the compositor in headless runs"
    data = ctl.blob("gkeep-ui-excerpt.py") + ("\n# %s\n" % q).encode()
    ctl.set_receipt(g, "S299", "gkeep-ui-excerpt.py", data, q)
    at = line_of_bytes(data, q)
    rep(g, ENTRY, ctl.entry_line("S299"),
        "**OBS** S299 %s (gkeep-ui-excerpt.py:%d)." % (q, at))
    return g


def fx_wrong_commit(g):
    """F-3b: S293 location = right host+repo, WRONG commit hash."""
    loc = ("https://raw.githubusercontent.com/hyprwm/Hyprland/"
           "0123456789abcdef0123456789abcdef01234567/src/layout/target/Target.cpp")
    rep(g, SRC, ctl.REAL["S293"][2], loc)
    return g


LONG_LINE = ("**CAVEAT** the applicator registers static sizing here although several later "
             "passes may still adjust the final box, which this entry deliberately does not "
             "restate as a quotation S291.")


def fx_long_line(g):
    """F-4b: a >120-char entry line naming S291 without its Gate quote."""
    assert len(LONG_LINE) > 120 and "static_.size = expr;" not in LONG_LINE
    g[ENTRY] = g[ENTRY] + "\n" + LONG_LINE + "\n"
    return g


def fx_flip_embedded(g):
    """F-6b: REFUSE reason whose only flip token is embedded in a larger word."""
    rep(g, LES, ctl.REFUSE,
        "REFUSE %s reason=this staging note is whenever-compatible and "
        "otherwise unreviewed content here" % ctl.PKG2)
    return g


def fx_qiita(g):
    """F-7b: localized-channel markers the reduced BAD_LOC tuple no longer holds."""
    g[ENTRY] = g[ENTRY] + "\nAlso summarized on qiita.com and zenn.dev as secondary channels.\n"
    return g


def fx_seven_pins(g):
    """F-8b: cite 7 of the 10 pinned receipts (drop S294, S295, S296)."""
    for i in ("S294", "S295", "S296"):
        rowline = [l for l in g[SRC].splitlines() if l.startswith("| %s |" % i)][0]
        g[SRC] = g[SRC].replace(rowline + "\n", "")
        g[ENTRY] = g[ENTRY].replace("source: %s - receipt\n" % i, "")
        g[ENTRY] = g[ENTRY].replace(ctl.entry_line(i) + "\n", "")
        gl = [l for l in g[LES].splitlines() if l.startswith("GATE %s " % i)][0]
        g[LES] = g[LES].replace(gl + "\n", "")
    return g


CASES = [
    ("F-2b-py-comment-quote", fx_comment_py, "V2-2b", "d"),
    ("F-3b-wrong-commit-url", fx_wrong_commit, "V2-3b", "e"),
    ("F-4b-long-naming-line", fx_long_line, "V2-4b", "g"),
    ("F-6b-flip-word-embedded", fx_flip_embedded, "V2-6b", "i"),
    ("F-7b-qiita-zenn-entry", fx_qiita, "V2-7b", "i"),
    ("F-8b-seven-of-ten-pins", fx_seven_pins, "V2-8b", "i"),
]

print("probe driver: pristine=%s" % PRISTINE)
for tag, fx, mutant, clause in CASES:
    g = fx({k: v for k, v in P.items()})
    rc0, v0, c0 = score(PRISTINE, g)
    mpath = os.path.join(S, "mutants", mutant + ".py")
    rc1, v1, c1 = score(mpath, g)
    ok = rc0 == 1 and rc1 == 0
    print("%-26s pristine rc=%d %s [%s] | %s rc=%d %s [%s] => %s"
          % (tag, rc0, v0, c0, mutant, rc1, v1, c1,
             "KILLS " + mutant if ok else "CHECK MANUALLY"))
