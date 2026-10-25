#!/usr/bin/env python3
"""Round-40 C1 controls: PRED-C1-r40-v1 scored over mutated live-mode tools.

Each mutant is the committed reference live tool (`../c1/ctl-ref-tool.py.txt`,
the reachability proof: 13/13 on the fixtures; it is a control, never the
delivered tool) with ONE defect, scored with the frozen counter's `--tool`
switch. The reference must reach fixtures=13/13; every mutant and the BASE
tool must score fixtures<13 (and the replay stub far less). Final line:
`CTL_C1: controls=N correct=K/N`.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r40-live.py")
REF = os.path.join(HERE, "..", "c1", "ctl-ref-tool.py.txt")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
REV = os.environ.get("MADO_CTL_REV", "master")

MUTANTS = {
    "M01-all-agree": ("def native_equal(form, declared, live, inherited=0):\n",
                      "def native_equal(form, declared, live, inherited=0):\n    return True\n"),
    "M02-raw-compare": ("def native_equal(form, declared, live, inherited=0):\n",
                        "def native_equal(form, declared, live, inherited=0):\n"
                        "    return declared.strip() == str(live).strip()\n"),
    "M03-bool-exact": ('    if v.startswith(("true", "on", "yes")):',
                       '    if v in ("true", "on", "yes"):'),
    "M04-gradient-angle-ignored": ('" %ddeg" % angle == str(live)',
                                   '" %ddeg" % 0 == str(live)'),
    "M05-gap-three-values-wrong": ("[n[0], n[1], n[2], n[1]]",
                                   "[n[0], n[1], n[2], n[0]]"),
    "M06-config-only-as-mismatch": ('row["agreement"] = "config-only"\n            row["live"] = None',
                                    'row["agreement"] = "mismatch"\n            row["live"] = None'),
    "M07-extra-argv": ("    try:\n        p = subprocess.run([hyprctl, \"getoption\"",
                       "    subprocess.run([hyprctl, \"version\"], "
                       "capture_output=True)\n    try:\n        p = subprocess.run"
                       "([hyprctl, \"getoption\""),
    "M08-set-ignored": ("if not isset or not native_equal",
                        "if not native_equal"),
    "M09-shadow-ignored": ('        elif options[row["key"]]["_decls"] > 1:\n            row["agreement"] = "agreement*"\n        else:\n            row["agreement"] = "agreement"\n    for key in probes',
                           '        else:\n            row["agreement"] = "agreement"\n    for key in probes'),
    "M10-hostile-probe-accepted": ('        if not k or k.startswith("-"):',
                                   '        if False:'),
    "M11-failure-swallowed": ('    if p.returncode != 0:\n        raise CtlError("%s: %s exited %d" % (key, hyprctl, p.returncode))',
                              '    if p.returncode != 0:\n        return None'),
    "M12-writes-config-root": ('        if args.live:\n',
                               '        if args.live:\n'
                               '            open(os.path.join(home, ".config", "hypr", "zz.tmp"), "w").write("x")\n'),
    "M13-no-normalisation-int": ("            return hl_int(d) == live\n",
                                 "            return d == str(live)\n"),
    "M15-angle-inheritance-absent": ('options[row["key"]].get("_angle", 0)',
                                     '0'),
    "M16-probe-key-without-argv-check": ('        rec = native_query(hyprctl, key)\n        if rec is None:\n            continue',
                                         '        rec = native_query(hyprctl, key)\n        if rec is None:\n            rec = ("str", "", False)'),
    "M14-live-field-dropped": ('        row["live"] = str(value)\n',
                               '        pass\n'),
}


def score(path):
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", LANE,
                        "--rev", REV, "--tool", path],
                       capture_output=True, text=True, env=ENV)
    lines = p.stdout.strip().splitlines()
    last = lines[-1] if lines else ""
    return last.split(": ", 1)[-1].split(" rev=")[0]


def main():
    ref = open(REF).read()
    tmp = tempfile.mkdtemp(prefix="mado-c1ctl-")
    results = []
    ok_all = True
    # reference: must reach 13/13 fixtures (clauses b/k are scored separately)
    ref_path = os.path.join(tmp, "ref.py")
    with open(ref_path, "w") as fh:
        fh.write(ref)
    r = score(ref_path)
    ref_ok = "fixtures=13/13" in r
    print("control=REF-reachability expected=fixtures=13/13 observed=%s ok=%d"
          % (r, ref_ok))
    results.append(ref_ok)
    base = subprocess.run(["git", "-C", LANE, "show", "master:tools/mado-options.py"],
                          capture_output=True, text=True, env=ENV).stdout
    base_path = os.path.join(tmp, "base.py")
    with open(base_path, "w") as fh:
        fh.write(base)
    r = score(base_path)
    ok = "fixtures=0/13" in r
    print("control=BASE-tool expected=fixtures=0/13 observed=%s ok=%d" % (r, ok))
    results.append(ok)
    for name, (old, new) in sorted(MUTANTS.items()):
        if old not in ref:
            print("control=%s MUTATION-TARGET-ABSENT ok=0" % name)
            results.append(False)
            continue
        path = os.path.join(tmp, name + ".py")
        with open(path, "w") as fh:
            fh.write(ref.replace(old, new, 1))
        r = score(path)
        m = None
        if "fixtures=" in r:
            m = int(r.split("fixtures=")[1].split("/")[0])
        ok = m is not None and m < 13
        print("control=%s expected=fixtures<13 observed=%s ok=%d" % (name, r, ok))
        results.append(ok)
    n = len(results)
    print("CTL_C1: controls=%d correct=%d/%d" % (n, sum(results), n))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
