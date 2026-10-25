#!/usr/bin/env python3
"""Liveness cross-check for the 16 C1 mutants: each survivor of the base
71-assertion --selftest must also be shown to actually change observable
behavior on the --live path (else it might be an equivalent mutant).

Hermetic: fixture config home + stub hyprctl (canned getoption -j replies,
argv logging, optional per-key exit-1 failure). No real compositor, no
sockets, no writes outside the mktemp scratch.

Scenarios per tool copy:
  S1 main live merge  --home H --live --hyprctl STUB --probe cursor:no_warps
  S2 hostile probes   ... --probe -bad --probe ""      (pristine: exit 2)
  S3 compositor fail  STUB_FAIL_KEY=general:border_size (pristine: exit 5)
Divergence in any of (exit, stdout, stderr, stub argv log, zz.tmp side file)
=> LIVE; identical everywhere => EQUIVALENT-on-harness.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/c1/ctl-ref-tool.py.txt"
CONTROLS = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/ctl/run-c1-controls.py"

spec = importlib.util.spec_from_file_location("c1ctl", CONTROLS)
c1ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1ctl)
MUTANTS = c1ctl.MUTANTS

CONF = """general {
    gaps_out = 4 8 12
    allow_tearing = yes
    border_size = 2
}
input {
    kb_layout = us
    repeat_rate = 0x19
}
misc {
    disable_autoreload = true
    trueish = trueish
}
group:groupbar {
    font_size = 12
}
decoration {
    col.active_border = rgba(33ccffee) rgba(00ff99ee) 45deg
    col.active_border = rgb(e68e0d)
    col.inactive_border = rgba(11ff22ee) 30deg
}
"""

TABLE = {
    "general:gaps_out": {"option": "general:gaps_out", "set": True,
                         "custom": "4 8 12 8"},
    "general:allow_tearing": {"option": "general:allow_tearing", "set": True,
                              "int": 0},
    "input:kb_layout": {"option": "input:kb_layout", "set": True, "str": "us"},
    "input:repeat_rate": {"option": "input:repeat_rate", "set": True, "int": 25},
    "misc:disable_autoreload": {"option": "misc:disable_autoreload",
                                "set": False, "int": 1},
    "misc:trueish": {"option": "misc:trueish", "set": True, "int": 1},
    "decoration:col.active_border": {"option": "decoration:col.active_border",
                                     "set": True, "custom": "ffe68e0d 45deg"},
    "decoration:col.inactive_border": {
        "option": "decoration:col.inactive_border", "set": True,
        "custom": "ee11ff22 30deg"},
    # group:groupbar:font_size and cursor:no_warps deliberately absent ->
    # stub prints `no such option` (exit 0).
}

STUB = """#!/usr/bin/env python3
import json, os, sys
argv = sys.argv[1:]
log = os.environ.get("STUB_LOG")
if log:
    with open(log, "a") as fh:
        fh.write(json.dumps(argv) + "\\n")
if argv and argv[0] == "version":
    print("stub version reply")
    sys.exit(0)
if len(argv) == 3 and argv[0] == "getoption" and argv[1] == "-j":
    key = argv[2]
    fail = os.environ.get("STUB_FAIL_KEY")
    if fail and key == fail:
        sys.exit(1)
    table = json.load(open(os.environ["STUB_TABLE"]))
    if key not in table:
        print("no such option")
        sys.exit(0)
    print(json.dumps(table[key]))
    sys.exit(0)
sys.exit(1)
"""


def build_fixture(tmp):
    home = os.path.join(tmp, "home")
    os.makedirs(os.path.join(home, ".config", "hypr"))
    with open(os.path.join(home, ".config", "hypr", "hyprland.conf"), "w") as fh:
        fh.write(CONF)
    stub = os.path.join(tmp, "stub-hyprctl")
    with open(stub, "w") as fh:
        fh.write(STUB)
    os.chmod(stub, 0o755)
    table = os.path.join(tmp, "table.json")
    with open(table, "w") as fh:
        json.dump(TABLE, fh)
    return home, stub, table


def scenario_run(tool, tmp, home, stub, table, scen):
    log = os.path.join(tmp, "stublog-%s" % scen)
    if os.path.exists(log):
        os.unlink(log)
    zzt = os.path.join(home, ".config", "hypr", "zz.tmp")
    if os.path.exists(zzt):
        os.unlink(zzt)
    env = dict(os.environ, STUB_TABLE=table, STUB_LOG=log)
    args = ["--home", home, "--live", "--hyprctl", stub]
    if scen == "S1":
        args += ["--probe", "cursor:no_warps"]
    elif scen == "S2":
        # `=`-form values reach main's own validator; bare `-bad` would be
        # rejected by argparse itself and mask the mutant.
        args += ["--probe=-bad", "--probe="]
    if scen == "S3":
        env["STUB_FAIL_KEY"] = "general:border_size"
    p = subprocess.run([sys.executable, "-I", tool] + args,
                       capture_output=True, text=True, cwd=tmp, env=env,
                       timeout=120)
    sig = (p.returncode, p.stdout, p.stderr,
           open(log).read() if os.path.exists(log) else "",
           os.path.exists(zzt))
    return sig


def main():
    ref = open(REF, encoding="utf-8").read()
    tmp = tempfile.mkdtemp(prefix="mutlive-")
    home, stub, table = build_fixture(tmp)

    pristine = os.path.join(tmp, "pristine.py")
    open(pristine, "w", encoding="utf-8").write(ref)
    base = {s: scenario_run(pristine, tmp, home, stub, table, s)
            for s in ("S1", "S2", "S3")}
    print("PRISTINE S1 rc=%d rows=%d zz=%s log_n=%d" % (
        base["S1"][0], len(json.loads(base["S1"][1])), base["S1"][4],
        len(base["S1"][3].splitlines())))
    rows = {r["key"]: r for r in json.loads(base["S1"][1])}
    for k in sorted(rows):
        print("   %-32s %-12s live=%r" % (k, rows[k].get("agreement"),
                                          rows[k].get("live")))
    print("PRISTINE S2 rc=%d err=%r" % (base["S2"][0], base["S2"][2].strip()))
    print("PRISTINE S3 rc=%d err=%r" % (base["S3"][0], base["S3"][2].strip()))

    print()
    for name in sorted(MUTANTS):
        old, new = MUTANTS[name]
        path = os.path.join(tmp, name + ".py")
        open(path, "w", encoding="utf-8").write(ref.replace(old, new, 1))
        diffs = []
        for s in ("S1", "S2", "S3"):
            sig = scenario_run(path, tmp, home, stub, table, s)
            if sig != base[s]:
                fields = [f for i, f in enumerate(("rc", "stdout", "stderr",
                                                   "stublog", "zz.tmp"))
                          if sig[i] != base[s][i]]
                diffs.append("%s(%s)" % (s, ",".join(fields)))
        print("%s %s" % (name, "LIVE via " + "+".join(diffs) if diffs
                         else "EQUIVALENT-on-harness"))
    print("SCRATCH=%s" % tmp)


if __name__ == "__main__":
    main()
