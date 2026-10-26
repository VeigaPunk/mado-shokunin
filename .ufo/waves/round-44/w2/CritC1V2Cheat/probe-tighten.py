#!/usr/bin/env python3
"""CritC1V2Cheat: candidate tightening probes for PRED-C1-r44-v2.

Two clauses the v2 counter does not have, measured on the reference and on each cheat:

  E'  invocation invariance (tightened clause e): the same client bytes and rule text produce the
      same stdout and rc (a) when invoked the way the instrument invokes the tool (file args inside a
      `mado-c1r44-*` temp tree) and (b) when invoked the way a user does (stdin pipe for clients, a
      rule file under a plausible `$HOME/.config/hypr`, cwd = that config dir).  v2's clause e holds
      the invocation fixed and varies only the sandbox, so an instrument-keyed tool is invisible to it.
  M   semantic mutant (the b5 replacement w1/CritC1Cheat section 2 proposed): a copy whose
      `client_fsmode` always returns 0 (state verdicts disabled) must FAIL its own selftest.

Inputs are the counter's own INVARIANT_INPUTS / GKCONF, imported from the frozen counter (read-only).
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.path.join(HERE, "..", "..", "..", "..", "..", "quality", "counters",
                       "c1-r44-geometry-states-v2.py")
COUNTER = os.path.abspath(COUNTER)
WORK = sys.argv[1] if len(sys.argv) > 1 else "/fast/scratch/hyaku/mado-r44/CritC1V2Cheat/probe"
TOOLS = sys.argv[2:] or ["ref-verified.py", "cheat-h-harness-gate.py", "cheat-i1-vacuous.py",
                         "cheat-i2-vacuous-detect.py", "cheat-j-honest-jsondecoder.py",
                         "cheat-j2-jsondecoder-gate-detect.py"]


def load(path):
    spec = importlib.util.spec_from_file_location("c1r44v2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = load(COUNTER)
GY = "/usr/bin" if os.path.isdir("/usr/bin") else "/bin"


def run(argv, cwd, env, stdin=None):
    p = subprocess.run([os.path.realpath(sys.executable), "-I"] + argv, cwd=cwd, env=env,
                       capture_output=True, timeout=60, input=stdin)
    return p.returncode, p.stdout


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    inst = os.path.join(WORK, "mado-c1r44-probe", hashlib.sha256(b"probe").hexdigest()[:12])
    real = os.path.join(WORK, "home", ".config", "hypr")
    bindir = os.path.join(WORK, "home", ".local", "lib", "mado")
    os.makedirs(inst)
    os.makedirs(real)
    os.makedirs(bindir)
    with open(os.path.join(real, "hyprland.conf"), "w") as fh:
        fh.write(mod.GKCONF)
    env_real = {"PATH": GY, "HOME": os.path.join(WORK, "home"), "LC_ALL": "C"}
    env_inst = {"PATH": GY, "HOME": "/nonexistent", "LC_ALL": "C"}
    rows = []
    for name in TOOLS:
        tool = os.path.join(HERE, name)
        src = open(tool).read()
        deployed = os.path.join(bindir, "mado-geometry.py")   # realistic install path, not a temp copy
        with open(deployed, "w") as fh:
            fh.write(src)
        # --- E': instrument invocation vs user invocation, same inputs
        same_e = True
        detail = []
        for fx in mod.INVARIANCE:
            raw = json.dumps(mod.INVARIANT_INPUTS[fx]).encode()
            cpath = os.path.join(inst, "c.json" if fx == "fs0" else "c-%s.json" % fx)
            rpath = os.path.join(inst, "r0.conf")
            with open(cpath, "wb") as fh:
                fh.write(raw)
            with open(rpath, "w") as fh:
                fh.write(mod.GKCONF)
            rc1, out1 = run([tool, "--clients", cpath, "--rules", rpath], inst, env_inst)
            rc2, out2 = run([deployed, "--clients", "-", "--rules",
                             os.path.join(real, "hyprland.conf")], real, env_real, stdin=raw)
            same_e &= rc1 == rc2 and out1 == out2
            detail.append("%s:%d" % (fx, int(rc1 == rc2 and out1 == out2)))
        # --- M: state-disabled copy must fail its own selftest
        mut = src.replace("\n        return f\n    return 0", "\n        return 0\n    return 0")
        assert mut != src, name + ": mutant site not found"
        mp = os.path.join(inst, "tool")
        os.makedirs(mp, exist_ok=True)
        mpath = os.path.join(mp, "mado-geometry.py")
        with open(mpath, "w") as fh:
            fh.write(mut)
        rc, out = run([mpath, "--selftest"], mp, env_inst)
        m = re.search(r"MADO_GEOMETRY_SELFTEST: (\d+)/(\d+) passed", out.decode("utf-8", "replace"))
        k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        killed_m = rc != 0 or not m or k != n
        rows.append((name, same_e, " ".join(detail), killed_m, rc, k, n))
    print("%-34s %-4s %-42s %-6s %s" % ("tool", "E'", "per-fixture", "M", "mutant selftest"))
    for name, same_e, detail, killed_m, rc, k, n in rows:
        print("%-34s %-4s %-42s %-6s rc=%s %d/%d" % (
            name, "ok" if same_e else "FAIL", detail, "kill" if killed_m else "PASS", rc, k, n))
    bad = [r[0] for r in rows if not r[1]]
    vac = [r[0] for r in rows if not r[3]]
    print("E' rejects: %s" % (", ".join(bad) if bad else "none"))
    print("M rejects: %s" % (", ".join(vac) if vac else "none"))


if __name__ == "__main__":
    main()
