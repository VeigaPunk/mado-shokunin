#!/usr/bin/env python3
"""mado round 27 quality: counter self-test, suite A (offline).

Gate over the two round-26 counters

    C1 = .ufo/waves/round-26/c1/count-v2.py   (animations table)
    C2 = .ufo/waves/round-26/c2/count.py      (binds table)

Exit 0 only when every behavioural check passes.  The gate is behavioural: the harness
surfaces of each counter (check_build, coredumps, snapshot, oracle, run_tool) are replaced
with synthetic fakes and the counter is then asked to judge synthetic tools.  No subject
hash, AST or byte pattern is pinned, no mutant text is blocklisted, and nothing about the
surrounding process, path or timing is inspected: a counter that behaves correctly passes,
a counter whose judgement is broken fails.

The round-26 self-test failed 2 of its 9 checks on the active C1 v2 counter because its
fake oracle answered the `version` verb with an animation table; the fake oracle here
answers `version` with the pinned Hyprland commit, so the version guard is exercised too.

Checks (55 behavioural probes + 1 fixed-inventory gate):

  C1  c1-perfect          perfect tool                        -> exit 0, TARGET_MET, 41/41
      c1-field-*          one node field wrong (6 fields)     -> exit 1, TARGET_MISSED
      c1-bezier-*         one bezier field wrong (5 fields)    -> exit 1, TARGET_MISSED
      c1-invalid-json     tool stdout is not JSON              -> exit 1, TARGET_MISSED
      c1-malformed        tool stdout is not [nodes,beziers]   -> exit 1, TARGET_MISSED
      c1-tool-exit        tool exits non-zero                  -> exit 1, TARGET_MISSED
      c1-near-perfect     40 of 41 cases right                 -> exit 1, TARGET_MISSED
      c1-drift            two BASE oracle runs disagree       -> exit 2, ORACLE_UNSTABLE
      c1-oracle-fail      every oracle call fails              -> exit 2, ORACLE_FAIL
      c1-version-guard    nested Hyprland commit is wrong      -> exit 2, ORACLE_VERSION
  C2  c2-perfect          perfect tool                        -> exit 0, TARGET_MET, 51/51
      c2-field-*          one bind field wrong (18 fields)    -> exit 1, TARGET_MISSED
      c2-invalid-json     tool stdout is not JSON              -> exit 1, TARGET_MISSED
      c2-malformed        tool stdout is not a list            -> exit 1, TARGET_MISSED
      c2-tool-exit        tool exits non-zero                  -> exit 1, TARGET_MISSED
      c2-near-perfect     50 of 51 cases right                 -> exit 1, TARGET_MISSED
      c2-embed            tool bytes hold a 40-char base arg   -> exit 1, embed_hits>=1
      c2-embed-desc       tool bytes hold a 40-char desc       -> exit 1, embed_hits>=1
      c2-drift            two BASE oracle runs disagree       -> exit 2, ORACLE_UNSTABLE
      c2-drift-superset   the two runs differ by one entry    -> exit 2, ORACLE_UNSTABLE
      c2-oracle-fail      every oracle call fails              -> exit 2, ORACLE_FAIL
      c2-extra-one        tool reports one entry too many      -> exit 1, TARGET_MISSED
      c2-extra-two        tool reports two entries too many    -> exit 1, TARGET_MISSED
      c2-missing-one      tool omits one entry                 -> exit 1, TARGET_MISSED
      c2-embed-at-threshold   12-char base arg in tool bytes  -> exit 1, embed_hits>=1
      c2-embed-below-threshold 11-char base arg in tool bytes -> exit 0, embed_hits=0
      c2-embed-desc-at-threshold   12-char base desc         -> exit 1, embed_hits>=1
      c2-embed-desc-below-threshold 11-char base desc        -> exit 0, embed_hits=0
      check-inventory     every required check was executed    -> missing/extra listed

Each `field` check changes exactly one field of the synthetic truth, so a counter that stops
comparing that field is caught by that check alone.  A changed field makes one entry missing
AND one entry extra at the same time, so the checks that break exactly one side of that
conjunction -- one extra entry, two extra entries, one missing entry -- are separate, and
so are the two sides of the embed threshold.

Offline: no Hyprland, no compositor, no display, no network, no /dev/dri.  All scratch lives
in one mkdtemp under TMPDIR (the counter's sandbox puts TMPDIR inside the run directory) and
is removed at the end; the counters' own temporary directories are redirected into it too.
Nothing outside that directory is written.

Usage:
  python3 -I counter-selftest.py --c1 PATH --c2 PATH --rev REV [--scratch DIR] [--keep]
Exit: 0 only when every check passes.  Prints `SELFTEST pass=N total=M`.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import threading

# The Hyprland v0.56.2 commit this wave pins.  The fake oracle reports it for the `version`
# verb so that the counter's version guard is exercised; it is the wave's pin, not a pin of
# any subject file.
HYPR_COMMIT = "efb50993780079460b0cbed1363e2166a2de1d9f"
VERSION_OK = {"commit": HYPR_COMMIT, "tag": "v0.56.2"}
VERSION_BAD = {"commit": "0" * 40, "tag": "v0.0.0"}

MARK_NAME = ".mado-selftest-near-perfect"
SEED = "27a1c0de5eed0001"

# The synthetic unperturbed tree both counters copy into their cases.  Its bind lines match
# the synthetic C2 base table (mask 64 / Q, W, E) so the counter's own case generator finds
# real bind lines that map to exactly one live entry, and its `source` line gives C1 a
# source graph to perturb.
SNAPSHOT_FILES = {
    ".config/hypr/hyprland.conf": (
        "$mainMod = SUPER\n"
        "bind = SUPER, Q, exec, kitty\n"
        "bind = SUPER, W, exec, firefox\n"
        "bezier = myBez, 0.1, 0.2, 0.3, 1\n"
        "animation = windows, 1, 5, myBez\n"
        "animation = fade, 1, 3, default\n"
        "source = ~/.config/hypr/binds.conf\n"
    ),
    ".config/hypr/binds.conf": "bind = SUPER, E, exec, thunar\n",
}


def c1_table():
    """The C1 truth: [nodes, beziers], the shape `hyprctl animations -j` prints."""
    return [[
        {"name": "windows", "overridden": False, "bezier": "myBez", "enabled": True,
         "speed": 5.0, "style": ""},
        {"name": "fade", "overridden": False, "bezier": "default", "enabled": True,
         "speed": 3.0, "style": "popin"},
        {"name": "layers", "overridden": False, "bezier": "linear", "enabled": False,
         "speed": 8.0, "style": "slide"},
    ], [
        {"name": "myBez", "X0": 0.1, "Y0": 0.2, "X1": 0.3, "Y1": 1.0},
        {"name": "default", "X0": 0.25, "Y0": 0.1, "X1": 0.25, "Y1": 1.0},
        {"name": "linear", "X0": 0.0, "Y0": 0.0, "X1": 1.0, "Y1": 1.0},
    ]]


def bind_entry(modmask, key, arg, description=""):
    return {"locked": False, "mouse": False, "release": False, "repeat": False, "longPress": False,
            "non_consuming": False, "auto_consuming": False, "has_description": bool(description),
            "modmask": modmask, "submap": "", "submap_universal": "false", "key": key, "keycode": 0,
            "catch_all": False, "description": description, "allow_input_capture": False,
            "dispatcher": "exec", "arg": arg}


C1_BASE = c1_table()
C2_BASE = [bind_entry(64, "Q", "kitty"), bind_entry(64, "W", "firefox"),
           bind_entry(64, "E", "thunar", "Files")]

# A 40-character base-table argument: the counter's embed eligibility (EMBED_MIN) must see
# it, a threshold of 1000 must not.
EMBED_ARG = "notify-send r27-embed-fixture-0123456789"
assert len(EMBED_ARG) == 40, len(EMBED_ARG)
C2_EMBED = json.loads(json.dumps(C2_BASE))
C2_EMBED[0]["arg"] = EMBED_ARG
# The same eligibility seen from the other side: the long string sits in a description, the
# args stay short, so a counter that scans only one of the two fields is caught.
C2_EMBED_DESC = json.loads(json.dumps(C2_BASE))
C2_EMBED_DESC[2]["description"] = EMBED_ARG

# The two sides of the embed-eligibility threshold.  The counter admits a base-table arg
# or description of EMBED_MIN (12) or more characters; an arg of exactly 12 characters
# must therefore be seen as a hit and an arg of exactly 11 must not be.  A threshold moved
# by one character in either direction is caught by one of the two.
EMBED_ARG_12 = "embed-arg-12"      # exactly 12 characters
EMBED_ARG_11 = "embed-arg-1"       # exactly 11 characters
assert len(EMBED_ARG_12) == 12, len(EMBED_ARG_12)
assert len(EMBED_ARG_11) == 11, len(EMBED_ARG_11)
C2_EMBED_12 = json.loads(json.dumps(C2_BASE))
C2_EMBED_12[0]["arg"] = EMBED_ARG_12
C2_EMBED_11 = json.loads(json.dumps(C2_BASE))
C2_EMBED_11[0]["arg"] = EMBED_ARG_11
# The same two lengths seen through the other field: the embed scan reads the arg and the
# description of every base entry.
C2_EMBED_12D = json.loads(json.dumps(C2_BASE))
C2_EMBED_12D[2]["description"] = EMBED_ARG_12
C2_EMBED_12D[2]["has_description"] = True
C2_EMBED_11D = json.loads(json.dumps(C2_BASE))
C2_EMBED_11D[2]["description"] = EMBED_ARG_11
C2_EMBED_11D[2]["has_description"] = True

# A second BASE oracle run that disagrees with the first by exactly one entry.  The
# counter compares the two runs and counts the entries missing from one and extra in the
# other; with a table that differs by a single added entry exactly one of those two counts
# is non-zero, so a guard that asks for both of them (a conjunction where the counter
# has a disjunction) is caught here, while the counter's own drift probe -- which
# replaces one field and so differs in both directions at once -- cannot see it.
C2_SUPERSET = json.loads(json.dumps(C2_BASE)) + [bind_entry(64, "X", "xterm")]

# Tool-side table defects the counter must judge as a mismatch.  The counter's verdict
# for a case is "nothing missing AND nothing extra", so a tool that reports one bind
# entry more than the truth, or two more, or one fewer, must each be judged a mismatch:
# a verdict that tolerates either side of that conjunction is a disjunction.
EXTRA_ONE = 'out.append(dict(out[0], key="EXTRA1", arg="extra1"))'
EXTRA_TWO = EXTRA_ONE + '\nout.append(dict(out[0], key="EXTRA2", arg="extra2"))'
MISSING_ONE = "out.pop(1)"

# One mutation per compared field: a counter that stops comparing that field alone is caught.
C1_NODE_FIELDS = [
    ("name", 'out[0][0]["name"] = "otherNode"'),
    ("overridden", 'out[0][0]["overridden"] = True'),
    ("bezier", 'out[0][0]["bezier"] = "linear"'),
    ("enabled", 'out[0][0]["enabled"] = False'),
    ("speed", 'out[0][0]["speed"] = 6.0'),
    ("style", 'out[0][0]["style"] = "gnomed"'),
]
C1_BEZ_FIELDS = [
    ("name", 'out[1][0]["name"] = "otherBez"'),
    ("x0", 'out[1][0]["X0"] = 0.9'),
    ("y0", 'out[1][0]["Y0"] = 0.9'),
    ("x1", 'out[1][0]["X1"] = 0.9'),
    ("y1", 'out[1][0]["Y1"] = 0.9'),
]
C2_FIELDS = [
    ("locked", 'out[0]["locked"] = True'),
    ("mouse", 'out[0]["mouse"] = True'),
    ("release", 'out[0]["release"] = True'),
    ("repeat", 'out[0]["repeat"] = True'),
    ("longpress", 'out[0]["longPress"] = True'),
    ("non-consuming", 'out[0]["non_consuming"] = True'),
    ("auto-consuming", 'out[0]["auto_consuming"] = True'),
    ("has-description", 'out[0]["has_description"] = True'),
    ("modmask", 'out[0]["modmask"] = 65'),
    ("submap", 'out[0]["submap"] = "s1"'),
    ("submap-universal", 'out[0]["submap_universal"] = "true"'),
    ("key", 'out[0]["key"] = "R"'),
    ("keycode", 'out[0]["keycode"] = 42'),
    ("catch-all", 'out[0]["catch_all"] = True'),
    ("description", 'out[2]["description"] = "Other"'),
    ("allow-input-capture", 'out[0]["allow_input_capture"] = True'),
    ("dispatcher", 'out[0]["dispatcher"] = "workspace"'),
    ("arg", 'out[0]["arg"] = "term"'),
]

# The required check inventory.  A check that silently disappears from the run makes the
# inventory gate fail; the total below is fixed independently of the number of recorded
# checks, so deleting a check (or the inventory gate itself) cannot pass unnoticed.
REQUIRED = (
    ["c1-perfect"]
    + ["c1-field-%s" % f for f, _ in C1_NODE_FIELDS]
    + ["c1-bezier-%s" % f for f, _ in C1_BEZ_FIELDS]
    + ["c1-invalid-json", "c1-malformed", "c1-tool-exit", "c1-near-perfect", "c1-drift",
       "c1-drift-bezier", "c1-oracle-fail", "c1-version-guard"]
    + ["c2-perfect"]
    + ["c2-field-%s" % f for f, _ in C2_FIELDS]
    + ["c2-invalid-json", "c2-malformed", "c2-tool-exit", "c2-near-perfect", "c2-embed",
       "c2-embed-desc", "c2-drift", "c2-oracle-fail"]
    + ["c2-extra-one", "c2-extra-two", "c2-missing-one", "c2-drift-superset",
       "c2-embed-at-threshold", "c2-embed-below-threshold",
       "c2-embed-desc-at-threshold", "c2-embed-desc-below-threshold"]
)
TOTAL = len(REQUIRED) + 1          # + the inventory gate itself


def sha(b):
    return hashlib.sha256(b).hexdigest()


def copy(obj):
    return json.loads(json.dumps(obj))


TOOL_SRC = '''#!/usr/bin/env python3
import json, os, sys
home = ""
argv = sys.argv[1:]
for i, a in enumerate(argv):
    if a == "--home" and i + 1 < len(argv):
        home = argv[i + 1]
BASE = json.loads(%(base)s)
MARK = %(mark)s
MODE = %(mode)s
if MODE == "nonjson":
    sys.stdout.write("this is not json at all\\n")
    sys.exit(0)
if MODE == "malformed":
    sys.stdout.write(json.dumps({"entries": "not a list"}) + "\\n")
    sys.exit(0)
if MODE == "exit":
    sys.stderr.write("tool failed on purpose\\n")
    sys.exit(3)
out = json.loads(json.dumps(BASE))
%(mut)s
sys.stdout.write(json.dumps(out) + "\\n")
'''


def write_tool(path, table, mode="perfect", mut=""):
    src = TOOL_SRC % {"base": json.dumps(json.dumps(table)), "mark": json.dumps(MARK_NAME),
                      "mode": json.dumps(mode), "mut": mut}
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)
    return path


def make_snapshot(ctx):
    """Offline stand-in for the harness snapshot: the synthetic tree, no host config read."""

    def snapshot(home_src, home_dst):
        ctx["snap"] = home_dst
        n = 0
        for rel, text in SNAPSHOT_FILES.items():
            path = os.path.join(home_dst, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            n += 1
        return n, sha(b"synthetic-r27-selftest-snapshot")

    return snapshot


class FakeOracle:
    """Offline stand-in for harness/oracle.py's oracle(): synthetic tables per verb, an
    optional drift fault (a different table from the second call on), total failure, and an
    optional marker written into the first case tree it is asked about."""

    def __init__(self, table, alt=None, version=VERSION_OK, fail=False, mark=False, ctx=None):
        self.table = table
        self.alt = alt
        self.version = version
        self.fail = fail
        self.mark = mark
        self.ctx = ctx if ctx is not None else {}
        self.calls = 0
        self.marked = False
        self.lock = threading.Lock()

    def __call__(self, case_home, work, verbs):
        with self.lock:
            self.calls += 1
            n = self.calls
        if self.fail:
            return None, "synthetic oracle failure"
        table = self.table if (self.alt is None or n == 1) else self.alt
        res = {}
        for v in verbs:
            if v == "version":
                res[v] = dict(self.version)
            else:
                res[v] = copy(table)
        snap = self.ctx.get("snap")
        if self.mark and snap and case_home != snap and not self.marked:
            self.marked = True
            try:
                with open(os.path.join(case_home, MARK_NAME), "w", encoding="utf-8") as fh:
                    fh.write("marked\n")
            except OSError:
                pass
        return res, ""


def make_run_tool():
    """Offline stand-in for the harness run_tool: the tool file is executed in-process (no
    bwrap, no compositor, no subprocess), its stdout is parsed exactly as the harness does."""

    def run_tool(tool, case_home, timeout=60):
        try:
            with open(tool, "r", encoding="utf-8") as fh:
                src = fh.read()
        except OSError as ex:
            return None, "tool unreadable: %r" % (ex,)
        buf = io.StringIO()
        errbuf = io.StringIO()
        old_argv = sys.argv
        sys.argv = ["tool.py", "--home", case_home]
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(errbuf):
                exec(compile(src, tool, "exec"), {"__name__": "__main__"})
        except SystemExit as ex:
            if ex.code not in (0, None):
                return None, "exit=%s stderr=%s" % (ex.code, errbuf.getvalue()[-200:].strip())
        except Exception as ex:  # noqa: BLE001
            return None, "tool raised %s: %r" % (type(ex).__name__, ex)
        finally:
            sys.argv = old_argv
        try:
            return json.loads(buf.getvalue()), ""
        except ValueError:
            return None, "stdout is not JSON"

    return run_tool


class TempShim:
    """Stands in for the counter's tempfile module: every temporary directory lands under this
    run's scratch root, which the self-test removes at the end."""

    def __init__(self, base):
        self.base = base
        self.n = 0
        self.lock = threading.Lock()

    def mkdtemp(self, prefix=None, dir=None, **kw):
        with self.lock:
            self.n += 1
            n = self.n
        tag = re.sub(r"[^A-Za-z0-9_.-]", "_", prefix or "d")
        path = os.path.join(self.base, "t%03d-%s" % (n, tag))
        os.makedirs(path, exist_ok=True)
        return path


def load_counter(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_counter(mod, args):
    buf = io.StringIO()
    old_argv = sys.argv
    sys.argv = ["count.py"] + args
    rc = None
    try:
        with contextlib.redirect_stdout(buf):
            rc = mod.main()
    except SystemExit as ex:
        rc = ex.code if isinstance(ex.code, int) else 2
    finally:
        sys.argv = old_argv
    return rc, buf.getvalue()


def pred(out):
    cp = re.search(r"cases_pass=(\d+)/(\d+)", out)
    eh = re.search(r"embed_hits=(\d+)", out)
    vd = re.search(r"verdict=([A-Z_]+)", out)
    return (int(cp.group(1)), int(cp.group(2))) if cp else (None, None), \
           int(eh.group(1)) if eh else None, \
           vd.group(1) if vd else None


KEEP_LINES = ("SETUP_ERROR", "ORACLE_UNSTABLE", "ORACLE_FAIL", "ORACLE_CHECK", "ORACLE_VERSION",
              "EMBED_HIT", "PRED-", "EXCEPTION", "tool=")


def interesting(out):
    lines = out.splitlines()
    picked = [ln for ln in lines if any(k in ln for k in KEEP_LINES)]
    cases = [ln for ln in lines if ln.startswith("CASE ")]
    if cases:
        picked += cases[:2]
        if len(cases) > 3:
            picked.append("... %d CASE lines omitted ..." % (len(cases) - 3))
        picked += cases[-1:]
    return picked


RESULTS = []


def record(name, ok, detail, out=""):
    RESULTS.append((name, bool(ok), detail))
    print("CHECK %-26s %s %s" % (name, "PASS" if ok else "FAIL", detail))
    for line in interesting(out):
        print("      " + line[:160])


def run_case(mod, run_dir, rev, tag, table, mode="perfect", mut="", alt=None,
             version=VERSION_OK, fail=False, mark=False):
    """Run one counter scenario with synthetic harness surfaces; returns (rc, stdout)."""
    ctx = {"snap": None}
    tool = write_tool(os.path.join(run_dir, "tool-%s.py" % tag), table, mode, mut)
    oracle = FakeOracle(table, alt=alt, version=version, fail=fail, mark=mark, ctx=ctx)
    mod.O.check_build = lambda: None
    mod.O.coredumps = lambda: 0
    mod.O.snapshot = make_snapshot(ctx)
    mod.O.oracle = oracle
    mod.O.run_tool = make_run_tool()
    mod.tempfile = TempShim(run_dir)
    args = [rev, "--tool-file", tool, "--seed", SEED, "--jobs", "1"]
    try:
        return run_counter(mod, args)
    except Exception as ex:  # noqa: BLE001 - a red run must report, not traceback
        return None, "EXCEPTION %s: %r" % (type(ex).__name__, ex)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--c1", required=True)
    ap.add_argument("--c2", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()

    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        os.environ.pop(k, None)
    base = a.scratch or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    run_dir = tempfile.mkdtemp(prefix="mado-selftest-", dir=base)
    try:
        c1b = open(a.c1, "rb").read()
        c2b = open(a.c2, "rb").read()
        print("MADO R27 QUALITY counter self-test (suite A; offline; synthetic tables; no Hyprland)")
        print("selftest sha256:%s" % sha(open(os.path.abspath(__file__), "rb").read()))
        print("c1=%s sha256:%s" % (a.c1, sha(c1b)))
        print("c2=%s sha256:%s" % (a.c2, sha(c2b)))
        print("rev=%s seed=%s scratch=%s" % (a.rev, SEED, run_dir))

        mods = {}
        for label, path in (("c1", a.c1), ("c2", a.c2)):
            try:
                mods[label] = load_counter(path, "mado_r27_q_%s" % label)
            except SystemExit as ex:
                print("SETUP_ERROR cannot load %s %s (exit %s)" % (label, path, ex.code))
                return 1
            except Exception as ex:  # noqa: BLE001
                print("SETUP_ERROR cannot load %s %s (%s: %r)" % (label, path, type(ex).__name__, ex))
                return 1
        c1, c2 = mods["c1"], mods["c2"]

        # ---- C1: the animations counter ------------------------------------------
        rc, out = run_case(c1, run_dir, a.rev, "c1-perfect", C1_BASE)
        (got, total), _, verdict = pred(out)
        record("c1-perfect", rc == 0 and verdict == "TARGET_MET" and got == total and total == 41,
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        for field, mut in C1_NODE_FIELDS:
            name = "c1-field-%s" % field
            rc, out = run_case(c1, run_dir, a.rev, name, C1_BASE, mut=mut)
            (got, total), _, verdict = pred(out)
            record(name, rc == 1 and verdict == "TARGET_MISSED" and got is not None and got < total,
                   "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        for field, mut in C1_BEZ_FIELDS:
            name = "c1-bezier-%s" % field
            rc, out = run_case(c1, run_dir, a.rev, name, C1_BASE, mut=mut)
            (got, total), _, verdict = pred(out)
            record(name, rc == 1 and verdict == "TARGET_MISSED" and got is not None and got < total,
                   "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c1, run_dir, a.rev, "c1-invalid-json", C1_BASE, mode="nonjson")
        (got, total), _, verdict = pred(out)
        record("c1-invalid-json", rc == 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c1, run_dir, a.rev, "c1-malformed", C1_BASE, mode="malformed")
        (got, total), _, verdict = pred(out)
        record("c1-malformed", rc == 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c1, run_dir, a.rev, "c1-tool-exit", C1_BASE, mode="exit")
        (got, total), _, verdict = pred(out)
        record("c1-tool-exit", rc == 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        # near-perfect: exactly one of the 41 cases is judged wrong.
        rc, out = run_case(c1, run_dir, a.rev, "c1-near-perfect", C1_BASE, mode="perfect",
                           mut='if os.path.exists(os.path.join(home, MARK)):\n'
                               '    out[0][0]["speed"] = 6.0',
                           mark=True)
        (got, total), _, verdict = pred(out)
        record("c1-near-perfect",
               rc == 1 and verdict == "TARGET_MISSED" and got == 40 and total == 41,
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        drift1 = copy(C1_BASE)
        drift1[0][0]["speed"] = 6.0
        rc, out = run_case(c1, run_dir, a.rev, "c1-drift", C1_BASE, alt=drift1)
        record("c1-drift", rc == 2 and "ORACLE_UNSTABLE" in out,
               "rc=%s ORACLE_UNSTABLE=%s" % (rc, "yes" if "ORACLE_UNSTABLE" in out else "no"), out)

        # the same guard seen from the other side: only the beziers drift
        drift1b = copy(C1_BASE)
        drift1b[1][0]["X0"] = 0.9
        rc, out = run_case(c1, run_dir, a.rev, "c1-drift-bezier", C1_BASE, alt=drift1b)
        record("c1-drift-bezier", rc == 2 and "ORACLE_UNSTABLE" in out,
               "rc=%s ORACLE_UNSTABLE=%s" % (rc, "yes" if "ORACLE_UNSTABLE" in out else "no"), out)

        rc, out = run_case(c1, run_dir, a.rev, "c1-oracle-fail", C1_BASE, fail=True)
        record("c1-oracle-fail", rc == 2 and "ORACLE_FAIL" in out,
               "rc=%s ORACLE_FAIL=%s" % (rc, "yes" if "ORACLE_FAIL" in out else "no"), out)

        rc, out = run_case(c1, run_dir, a.rev, "c1-version-guard", C1_BASE, version=VERSION_BAD)
        record("c1-version-guard", rc == 2 and "ORACLE_VERSION" in out,
               "rc=%s ORACLE_VERSION=%s" % (rc, "yes" if "ORACLE_VERSION" in out else "no"), out)

        # ---- C2: the binds counter ----------------------------------------------
        rc, out = run_case(c2, run_dir, a.rev, "c2-perfect", C2_BASE)
        (got, total), eh, verdict = pred(out)
        record("c2-perfect",
               rc == 0 and verdict == "TARGET_MET" and got == total and total == 51 and eh == 0,
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        for field, mut in C2_FIELDS:
            name = "c2-field-%s" % field
            rc, out = run_case(c2, run_dir, a.rev, name, C2_BASE, mut=mut)
            (got, total), _, verdict = pred(out)
            record(name, rc == 1 and verdict == "TARGET_MISSED" and got is not None and got < total,
                   "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-invalid-json", C2_BASE, mode="nonjson")
        (got, total), _, verdict = pred(out)
        record("c2-invalid-json", rc == 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-malformed", C2_BASE, mode="malformed")
        (got, total), _, verdict = pred(out)
        record("c2-malformed", rc == 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-tool-exit", C2_BASE, mode="exit")
        (got, total), _, verdict = pred(out)
        record("c2-tool-exit", rc == 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-near-perfect", C2_BASE, mode="perfect",
                           mut='if os.path.exists(os.path.join(home, MARK)):\n'
                               '    out[0]["arg"] = "term"',
                           mark=True)
        (got, total), _, verdict = pred(out)
        record("c2-near-perfect",
               rc == 1 and verdict == "TARGET_MISSED" and got == 50 and total == 51,
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-embed", C2_EMBED)
        (got, total), eh, verdict = pred(out)
        record("c2-embed",
               rc == 1 and verdict == "TARGET_MISSED" and eh is not None and eh >= 1,
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-embed-desc", C2_EMBED_DESC)
        (got, total), eh, verdict = pred(out)
        record("c2-embed-desc",
               rc == 1 and verdict == "TARGET_MISSED" and eh is not None and eh >= 1,
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        # The verdict for one case is "nothing missing AND nothing extra".  A tool that
        # reports an entry the truth does not have (one extra entry, or two) or omits an
        # entry the truth has breaks exactly one side of that conjunction, so each side
        # is probed on its own: a verdict that tolerates either side accepts the broken
        # table.  The per-field probes cannot see this, because a changed field makes one
        # entry missing AND one entry extra at the same time.
        rc, out = run_case(c2, run_dir, a.rev, "c2-extra-one", C2_BASE, mut=EXTRA_ONE)
        (got, total), _, verdict = pred(out)
        record("c2-extra-one",
               rc == 1 and verdict == "TARGET_MISSED" and got is not None and got < total,
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-extra-two", C2_BASE, mut=EXTRA_TWO)
        (got, total), _, verdict = pred(out)
        record("c2-extra-two",
               rc == 1 and verdict == "TARGET_MISSED" and got is not None and got < total,
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-missing-one", C2_BASE, mut=MISSING_ONE)
        (got, total), _, verdict = pred(out)
        record("c2-missing-one",
               rc == 1 and verdict == "TARGET_MISSED" and got is not None and got < total,
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        # The embed threshold from both sides.  The counter admits a base-table arg or
        # description of EMBED_MIN (12) or more characters: a string of exactly 12
        # characters must be reported as a hit and a string of exactly 11 must not be.
        # A threshold moved by one character in either direction is caught by one of the
        # two, and the long-string probe above cannot see it (40 characters is eligible
        # under any threshold near 12).
        rc, out = run_case(c2, run_dir, a.rev, "c2-embed-at-threshold", C2_EMBED_12)
        (got, total), eh, verdict = pred(out)
        record("c2-embed-at-threshold",
               rc == 1 and verdict == "TARGET_MISSED" and eh is not None and eh >= 1,
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-embed-below-threshold", C2_EMBED_11)
        (got, total), eh, verdict = pred(out)
        record("c2-embed-below-threshold",
               rc == 0 and verdict == "TARGET_MET" and eh == 0 and got == total,
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-embed-desc-at-threshold", C2_EMBED_12D)
        (got, total), eh, verdict = pred(out)
        record("c2-embed-desc-at-threshold",
               rc == 1 and verdict == "TARGET_MISSED" and eh is not None and eh >= 1,
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-embed-desc-below-threshold", C2_EMBED_11D)
        (got, total), eh, verdict = pred(out)
        record("c2-embed-desc-below-threshold",
               rc == 0 and verdict == "TARGET_MET" and eh == 0 and got == total,
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        drift2 = copy(C2_BASE)
        drift2[0]["arg"] = "term"
        rc, out = run_case(c2, run_dir, a.rev, "c2-drift", C2_BASE, alt=drift2)
        record("c2-drift", rc == 2 and "ORACLE_UNSTABLE" in out,
               "rc=%s ORACLE_UNSTABLE=%s" % (rc, "yes" if "ORACLE_UNSTABLE" in out else "no"), out)

        # The same guard seen from the side the field-replacement drift cannot reach.
        # The counter compares the two BASE oracle runs and asks whether the counts of
        # missing and extra entries differ; a field replacement makes one entry missing
        # AND one entry extra, so both counts are non-zero at once and a guard that asks
        # for both of them still fires.  A second run whose table differs from the first
        # by one *added* entry leaves exactly one of the two counts non-zero, so a guard
        # that asks for both of them misses the disagreement and lets the run continue.
        rc, out = run_case(c2, run_dir, a.rev, "c2-drift-superset", C2_BASE, alt=C2_SUPERSET)
        record("c2-drift-superset", rc == 2 and "ORACLE_UNSTABLE" in out,
               "rc=%s ORACLE_UNSTABLE=%s" % (rc, "yes" if "ORACLE_UNSTABLE" in out else "no"), out)

        rc, out = run_case(c2, run_dir, a.rev, "c2-oracle-fail", C2_BASE, fail=True)
        record("c2-oracle-fail", rc == 2 and "ORACLE_FAIL" in out,
               "rc=%s ORACLE_FAIL=%s" % (rc, "yes" if "ORACLE_FAIL" in out else "no"), out)

        # ---- fixed required check inventory --------------------------------------
        names = [n for n, _, _ in RESULTS]
        missing = [n for n in REQUIRED if n not in names]
        extra = [n for n in names if n not in REQUIRED]
        record("check-inventory", not missing and not extra,
               "missing=%s extra=%s" % (",".join(missing) or "none", ",".join(extra) or "none"))

        npass = sum(1 for _, ok, _ in RESULTS if ok)
        if len(RESULTS) != TOTAL:
            print("INVENTORY recorded=%d expected=%d" % (len(RESULTS), TOTAL))
            npass = -1
        print()
        print("SELFTEST pass=%d total=%d" % (npass, TOTAL))
        if npass != TOTAL:
            print("FAILED %s" % ",".join(name for name, ok, _ in RESULTS if not ok))
        rc = 0 if npass == TOTAL else 1
        print("exit=%d" % rc)
        return rc
    finally:
        if a.keep:
            print("kept scratch=%s" % run_dir)
        else:
            shutil.rmtree(run_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
