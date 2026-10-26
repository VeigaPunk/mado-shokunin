#!/usr/bin/env python3
"""tighten-check - a *proposed* tightening of PRED-C1-r45, scored beside the frozen predicate.

Not part of the lane's counting: this file only demonstrates that three semantics-free invariance checks
keep the reference (.ufo/waves/round-45/l1-draft/mado-monitors.py) MET while the controls that reach
TARGET_MET by table lookup or by loading the predicate fail them:

  serialize    a list dump written with sorted keys and no whitespace (json.dumps(..., sort_keys=True,
               separators=(",", ":"))) must produce byte-identical expected output - the tool reads fields,
               not JSON bytes;
  extra-config one more config argument holding a single comment line (no monitor line, no monitorv2)
               must produce byte-identical expected output - it contributes 0 to lines/v2/rules;
  reorder      for a dump of two or more outputs, the dump reversed must produce the same rule lines and
               the same summary with the MADO_MON_OUTPUT lines in the reversed order - outputs are reported
               in dump order.

Usage: tighten-check.py --repo R --rev V --work W. Prints one line per fixture case and a final
`TIGHTEN-C1: base=K/F serialize=K/F extra=K/F reorder=K/G verdict=<MET|MISSED> rev=<hash>`.
It reuses the frozen predicate's FIXTURES/names/subst by executing quality/counters/c1-r45-monitors.py, so
the cases are the predicate's own cases.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

COUNTER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..",
                       "quality", "counters", "c1-r45-monitors.py")

ns = {"__name__": "c1r45_predicate", "__file__": COUNTER}
exec(compile(open(COUNTER, "rb").read(), COUNTER, "exec"), ns)
FIXTURES, names, subst, git = ns["FIXTURES"], ns["names"], ns["subst"], ns["git"]
TOOL = ns["TOOL"]


def run_case(tool, work, fx, table, raw, cfgs, expect, rc_want):
    d = tempfile.mkdtemp(dir=work, prefix="tc-")
    home = os.path.join(d, "home")
    os.makedirs(home)
    dp = os.path.join(d, "monitors.json")
    with open(dp, "wb") as f:
        f.write(raw)
    args = ["--monitors", dp]
    for k, text in enumerate(cfgs):
        cp = os.path.join(d, "c%d.conf" % k)
        if text == "<DIR>":
            os.makedirs(cp)
        else:
            with open(cp, "w") as f:
                f.write(text)
        args += ["--config", cp]
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
           "HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}
    try:
        p = subprocess.run([sys.executable, "-I", tool] + args, capture_output=True, cwd=d, env=env,
                           timeout=10)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    want = "".join(l + "\n" for l in expect)
    got = p.stdout.decode("utf-8", "replace")
    ok = p.returncode == rc_want and got == want and p.stderr == b""
    return ok, "" if ok else "rc=%d/%d stderr=%d got=%r" % (p.returncode, rc_want, len(p.stderr), got[-240:])


def cases(fx, table):
    """Yield (variant, raw, configs, expected, rc) for one fixture."""
    label, configs, dump, stdin, expect, rc_want = fx
    if isinstance(configs, list):
        cfgs = [subst(t, table) for t in configs]
    elif configs == "usage":
        cfgs = []
    else:
        cfgs = ["<DIR>"]
    if isinstance(dump, bytes):
        raw = dump
        dump_obj = None
    else:
        dump_obj = subst(dump, table)
        raw = json.dumps(dump_obj, indent=2).encode()
    if cfgs is not None and (configs != "usage" or True):
        yield "base", raw, cfgs, expect, rc_want
    if dump_obj is not None:
        yield "serialize", json.dumps(dump_obj, sort_keys=True, separators=(",", ":")).encode(), cfgs, expect, rc_want
        if len(dump_obj) >= 2:
            outs = [l for l in expect if l.startswith("MADO_MON_OUTPUT:")]
            pos = [i for i, l in enumerate(expect) if l.startswith("MADO_MON_OUTPUT:")]
            exp = list(expect)
            for i, p in enumerate(pos):
                exp[p] = outs[-1 - i]
            yield "reorder", json.dumps(list(reversed(dump_obj)), indent=2).encode(), cfgs, exp, rc_want
    if cfgs:
        yield "extra-config", raw, cfgs + ["# no monitor line here\n"], expect, rc_want


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int, default=45)
    a = ap.parse_args()
    if not os.path.isdir(a.work):
        print("TIGHTEN-C1: SETUP work dir missing")
        return 2
    work = tempfile.mkdtemp(dir=a.work, prefix="tighten-")
    try:
        full = git(a.repo, "rev-parse", "--verify", a.rev + "^{commit}")
        if full is None:
            print("TIGHTEN-C1: SETUP bad rev")
            return 2
        full = full.decode().strip()
        blob = git(a.repo, "show", "%s:%s" % (full, TOOL))
        if blob is None:
            print("TIGHTEN-C1: base=0/0 serialize=0/0 extra=0/0 reorder=0/0 verdict=MISSED tool=absent rev=%s" % full)
            return 1
        tdir = tempfile.mkdtemp(dir=work, prefix="tool-")
        tool = os.path.join(tdir, "mado-monitors.py")
        with open(tool, "wb") as f:
            f.write(blob)
        table = names(a.seed)
        counts = {"base": [0, 0], "serialize": [0, 0], "extra-config": [0, 0], "reorder": [0, 0]}
        for fx in FIXTURES:
            for variant, raw, cfgs, expect, rc in cases(fx, table):
                expect = [subst(l, table) for l in expect]
                ok, why = run_case(tool, work, fx, table, raw, cfgs, expect, rc)
                counts[variant][1] += 1
                counts[variant][0] += ok
                if not ok:
                    print("TIGHTEN-C1 case=%s variant=%s FAIL %s" % (fx[0], variant, why))
        met = all(c[0] == c[1] and c[1] > 0 for c in counts.values())
        print("TIGHTEN-C1: base=%d/%d serialize=%d/%d extra=%d/%d reorder=%d/%d verdict=%s rev=%s" % (
            counts["base"][0], counts["base"][1], counts["serialize"][0], counts["serialize"][1],
            counts["extra-config"][0], counts["extra-config"][1], counts["reorder"][0], counts["reorder"][1],
            "MET" if met else "MISSED", full))
        return 0 if met else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
