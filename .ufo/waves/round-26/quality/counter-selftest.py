#!/usr/bin/env python3
"""mado round 26 quality R2: counter self-test, offline (repairs the round-25 spot-check defect
"surviving counter mutants skip-oracle-check and embed-threshold-1000").

The frozen counters' drift guard and embed eligibility were only inside conditions nobody had
ever made false, so a counter with `if False:` in place of the ORACLE_UNSTABLE guard or with
EMBED_MIN raised to 1000 produced the same receipts as the frozen counter on every input the
round-25 probe had. This self-test imports c1/count.py and c2/count.py by path, replaces their
harness surfaces with offline synthetic fakes, and scores the guards directly:

  c1-perfect / c2-perfect      perfect tool                        -> exit 0, TARGET_MET, N/N
  c1-one-field / c2-one-field  one field of one table entry wrong  -> exit 1, TARGET_MISSED
  c1-drift / c2-drift          two BASE oracle runs disagree       -> exit 2, ORACLE_UNSTABLE
  c2-embed                     tool bytes hold a 40-char base arg  -> embed_hits>=1, exit 1
  c1-oracle-fail / c2-oracle-fail  every oracle call fails          -> exit 2, ORACLE_FAIL

The drift and embed checks are the two unfalsified checks from the round-25 spot-check: a counter
with the guard skipped cannot report ORACLE_UNSTABLE, and a counter with EMBED_MIN=1000 cannot
count a 40-char arg (40 < 1000). Run with --c1/--c2 pointed at mutated scratch copies to see the
checks go red; the frozen bytes are never edited here.

Monkeypatches (on each counter module, after its own pinned imports succeed):
  O.check_build -> no-op        (no harness binaries needed)
  O.coredumps   -> 0            (no coredumpctl)
  O.snapshot    -> synthetic Hyprland tree
  O.oracle      -> synthetic tables, a call-order drift fault, or total failure
  O.run_tool    -> plain `python3 -I <tool> --home DIR` (no bwrap, no compositor)
  tempfile      -> shim rooted at this run's scratch directory
Nothing here starts Hyprland, touches a display, reads the home config, or uses the network.

Usage:
  python3 -I counter-selftest.py [--c1 PATH] [--c2 PATH] [--rev REV] [--scratch DIR] [--keep]
Exit: 0 only when every check passes. Prints `SELFTEST pass=N total=M`.
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
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
R26 = os.path.join(LANE, ".ufo/waves/round-26")
DEFAULT_C1 = os.path.join(R26, "c1/count.py")
DEFAULT_C2 = os.path.join(R26, "c2/count.py")
SCRATCH_BASE = "/fast/scratch/hyaku/mado-r26"
PIN_C1 = "f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd"
PIN_C2 = "b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8"
SEED = "0badc0de12345678"

# The synthetic unperturbed tree both counters copy into their cases. Its bind lines match the
# synthetic C2 base table (mask 64 / Q, W, E) so count-v3 REWRITE finds real bind lines that map
# to exactly one live entry, and its `source` line gives C1 a source graph to perturb.
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


def c1_table(style_windows=""):
    return [[
        {"name": "windows", "overridden": False, "bezier": "myBez", "enabled": True,
         "speed": 5.0, "style": style_windows},
        {"name": "fade", "overridden": False, "bezier": "default", "enabled": True,
         "speed": 3.0, "style": "popin"},
        {"name": "layers", "overridden": False, "bezier": "linear", "enabled": False,
         "speed": 8.0, "style": "slide"},
    ], [
        {"name": "myBez", "X0": 0.1, "Y0": 0.2, "X1": 0.3, "Y1": 1.0},
        {"name": "default", "X0": 0.25, "Y0": 0.1, "X1": 0.25, "Y1": 1.0},
    ]]


def bind_entry(modmask, key, arg, description=""):
    return {"locked": False, "mouse": False, "release": False, "repeat": False, "longPress": False,
            "non_consuming": False, "auto_consuming": False, "has_description": bool(description),
            "modmask": modmask, "submap": "", "submap_universal": "false", "key": key, "keycode": 0,
            "catch_all": False, "description": description, "allow_input_capture": False,
            "dispatcher": "exec", "arg": arg}


C1_BASE = c1_table("")
C1_OFF = c1_table("gnomed")          # one field of one node: style
C1_DRIFT = c1_table("")
C1_DRIFT[0][0]["speed"] = 6.0        # BASE#2 disagreement on exactly one field

C2_BASE = [bind_entry(64, "Q", "kitty"), bind_entry(64, "W", "firefox"),
           bind_entry(64, "E", "thunar", "Files")]
C2_OFF = json.loads(json.dumps(C2_BASE))          # one field of one bind: arg
C2_OFF[0]["arg"] = "term"
C2_DRIFT = json.loads(json.dumps(C2_BASE))
C2_DRIFT[1]["key"] = "X"                          # BASE#2 disagreement on exactly one field
                                                  # (not `arg`, so the field-dropped mutant
                                                  #  below cannot mask this guard by accident)

EMBED_ARG = "notify-send r26-embed-fixture-0123456789"
assert len(EMBED_ARG) == 40, len(EMBED_ARG)
C2_EMBED = json.loads(json.dumps(C2_BASE))
C2_EMBED[0]["arg"] = EMBED_ARG                    # a 40-char base-table arg: EMBED_MIN=12 sees
                                                  # it, a >=1000 threshold cannot


def sha(b):
    return hashlib.sha256(b).hexdigest()


def make_snapshot(home_src, home_dst):
    total = 0
    for rel, text in SNAPSHOT_FILES.items():
        path = os.path.join(home_dst, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        total += 1
    return total, sha(b"synthetic-r26-selftest-snapshot")


class FakeOracle:
    """Offline stand-in for harness/oracle.py's oracle(): returns a synthetic table for the verb,
    optionally a different table on every call after the first (the drift fault), or failure."""

    def __init__(self, verb, first, later=None, fail=False):
        self.verb = verb
        self.first = first
        self.later = later if later is not None else first
        self.fail = fail
        self.calls = 0
        self.lock = threading.Lock()

    def __call__(self, case_home, work, verbs):
        with self.lock:
            self.calls += 1
            n = self.calls
        if self.fail:
            return None, "synthetic oracle failure"
        table = self.first if n == 1 else self.later
        return {v: json.loads(json.dumps(table)) for v in verbs}, ""


def make_run_tool(python):
    def run_tool(tool, case_home, timeout=60):
        env = {"PATH": "/usr/bin", "HOME": case_home}
        try:
            p = subprocess.run([python, "-I", tool, "--home", case_home],
                               capture_output=True, timeout=timeout, env=env)
        except subprocess.TimeoutExpired:
            return None, "tool timed out"
        if p.returncode != 0:
            return None, "exit=%d stderr=%s" % (
                p.returncode, p.stderr.decode(errors="replace")[-200:].replace("\n", " | "))
        try:
            return json.loads(p.stdout), ""
        except ValueError:
            return None, "stdout is not JSON"

    return run_tool


class TempShim:
    """Stands in for the counter's `tempfile` module: every temporary directory lands under this
    run's scratch root, which the self-test removes at the end."""

    def __init__(self, base):
        self.base = base

    def mkdtemp(self, prefix=None, dir=None):
        return tempfile.mkdtemp(prefix=prefix or "q-", dir=self.base)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_tool(path, payload):
    src = ("#!/usr/bin/env python3\n"
           "import argparse, json\n"
           "ap = argparse.ArgumentParser()\n"
           "ap.add_argument('--home')\n"
           "ap.parse_args()\n"
           "PAYLOAD = %r\n"
           "print(json.dumps(PAYLOAD))\n" % (payload,))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)


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


def parse_pred(out):
    cp = re.search(r"cases_pass=(\d+)/(\d+)", out)
    eh = re.search(r"embed_hits=(\d+)", out)
    vd = re.search(r"verdict=([A-Z_]+)", out)
    return (int(cp.group(1)), int(cp.group(2))) if cp else (None, None), \
           int(eh.group(1)) if eh else None, \
           vd.group(1) if vd else None


KEEP_LINES = ("SETUP_ERROR", "ORACLE_UNSTABLE", "ORACLE_FAIL", "ORACLE_CHECK", "EMBED_HIT", "PRED-",
              "EXCEPTION")


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


CHECKS = []


def record(name, ok, detail, out):
    CHECKS.append((name, ok, detail))
    print("CHECK %-18s %s %s" % (name, "PASS" if ok else "FAIL", detail))
    for line in interesting(out):
        print("      " + line[:160])


def scenario(mod, run_dir, rev, name, payload, oracle):
    tool = os.path.join(run_dir, "tool-" + name + ".py")
    write_tool(tool, payload)
    mod.O.check_build = lambda: None
    mod.O.coredumps = lambda: 0
    mod.O.snapshot = make_snapshot
    mod.O.oracle = oracle
    mod.O.run_tool = make_run_tool(sys.executable)
    mod.tempfile = TempShim(run_dir)
    args = [rev, "--tool-file", tool, "--seed", SEED, "--jobs", "1"]
    try:
        return run_counter(mod, args)
    except Exception as ex:  # noqa: BLE001 - a red run must report, not traceback
        return None, "EXCEPTION %s: %r" % (type(ex).__name__, ex)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--c1", default=DEFAULT_C1)
    ap.add_argument("--c2", default=DEFAULT_C2)
    ap.add_argument("--rev", default="05319e0f")
    ap.add_argument("--scratch", default=SCRATCH_BASE)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()

    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        os.environ.pop(k, None)
    os.makedirs(a.scratch, exist_ok=True)
    run_dir = tempfile.mkdtemp(prefix="q-r2-selftest-", dir=a.scratch)
    try:
        c1b = open(a.c1, "rb").read()
        c2b = open(a.c2, "rb").read()
        print("MADO R26 QUALITY R2 counter self-test (offline; synthetic tables; no Hyprland)")
        print("selftest sha256:%s" % sha(open(os.path.abspath(__file__), "rb").read()))
        print("c1=%s sha256:%s pin=%s" % (a.c1, sha(c1b),
                                          "yes" if sha(c1b) == PIN_C1 else "no(override/mutant)"))
        print("c2=%s sha256:%s pin=%s" % (a.c2, sha(c2b),
                                          "yes" if sha(c2b) == PIN_C2 else "no(override/mutant)"))
        print("rev=%s seed=%s scratch=%s" % (a.rev, SEED, run_dir))

        c1 = load_module(a.c1, "q_r2_c1")
        c2 = load_module(a.c2, "q_r2_c2")

        rc, out = scenario(c1, run_dir, a.rev, "c1-perfect", C1_BASE,
                           FakeOracle("animations", C1_BASE))
        (got, total), _, verdict = parse_pred(out)
        record("c1-perfect", rc == 0 and verdict == "TARGET_MET" and got == total and total == 41,
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = scenario(c1, run_dir, a.rev, "c1-one-field", C1_OFF,
                           FakeOracle("animations", C1_BASE))
        (got, total), _, verdict = parse_pred(out)
        record("c1-one-field", rc == 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = scenario(c1, run_dir, a.rev, "c1-drift", C1_BASE,
                           FakeOracle("animations", C1_BASE, C1_DRIFT))
        record("c1-drift", rc == 2 and "ORACLE_UNSTABLE" in out,
               "rc=%s ORACLE_UNSTABLE=%s" % (rc, "yes" if "ORACLE_UNSTABLE" in out else "no"), out)

        rc, out = scenario(c1, run_dir, a.rev, "c1-oracle-fail", C1_BASE,
                           FakeOracle("animations", C1_BASE, fail=True))
        record("c1-oracle-fail", rc == 2 and "ORACLE_FAIL" in out,
               "rc=%s ORACLE_FAIL=%s" % (rc, "yes" if "ORACLE_FAIL" in out else "no"), out)

        rc, out = scenario(c2, run_dir, a.rev, "c2-perfect", C2_BASE,
                           FakeOracle("binds", C2_BASE))
        (got, total), eh, verdict = parse_pred(out)
        record("c2-perfect", rc == 0 and verdict == "TARGET_MET" and got == total and total == 51
               and eh == 0,
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        rc, out = scenario(c2, run_dir, a.rev, "c2-one-field", C2_OFF,
                           FakeOracle("binds", C2_BASE))
        (got, total), _, verdict = parse_pred(out)
        record("c2-one-field", rc == 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s verdict=%s" % (rc, got, total, verdict), out)

        rc, out = scenario(c2, run_dir, a.rev, "c2-embed", C2_EMBED,
                           FakeOracle("binds", C2_EMBED))
        (got, total), eh, verdict = parse_pred(out)
        record("c2-embed", rc == 1 and eh is not None and eh >= 1 and verdict == "TARGET_MISSED",
               "rc=%s cases_pass=%s/%s embed_hits=%s verdict=%s" % (rc, got, total, eh, verdict), out)

        rc, out = scenario(c2, run_dir, a.rev, "c2-drift", C2_BASE,
                           FakeOracle("binds", C2_BASE, C2_DRIFT))
        record("c2-drift", rc == 2 and "ORACLE_UNSTABLE" in out,
               "rc=%s ORACLE_UNSTABLE=%s" % (rc, "yes" if "ORACLE_UNSTABLE" in out else "no"), out)

        rc, out = scenario(c2, run_dir, a.rev, "c2-oracle-fail", C2_BASE,
                           FakeOracle("binds", C2_BASE, fail=True))
        record("c2-oracle-fail", rc == 2 and "ORACLE_FAIL" in out,
               "rc=%s ORACLE_FAIL=%s" % (rc, "yes" if "ORACLE_FAIL" in out else "no"), out)

        npass = sum(1 for _, ok, _ in CHECKS if ok)
        total = len(CHECKS)
        print()
        print("SELFTEST pass=%d total=%d" % (npass, total))
        if npass != total:
            print("FAILED %s" % ",".join(name for name, ok, _ in CHECKS if not ok))
        rc = 0 if npass == total else 1
        print("exit=%d" % rc)
        return rc
    finally:
        if a.keep:
            print("kept scratch=%s" % run_dir)
        else:
            shutil.rmtree(run_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
