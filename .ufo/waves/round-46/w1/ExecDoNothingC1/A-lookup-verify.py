#!/usr/bin/env python3
"""Local (no-bwrap) check of an A-LOOKUP style control against the frozen fixtures, in three tables.

Mirrors quality/counters/c1-r46-devices.py run_fixture() exactly (same file writing, same argv, same comparison)
but without the sandbox, so an attack tool can be iterated quickly. Not evidence on its own: the scored number
comes from the frozen counter.

Usage: A-lookup-verify.py <tool.py> [nonce]
"""
import importlib.util
import json
import os
import random
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CTR = os.path.join(LANE, "quality/counters/c1-r46-devices.py")


def load_ctr():
    spec = importlib.util.spec_from_file_location("ctr", CTR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    c = load_ctr()
    tool = os.path.abspath(sys.argv[1])
    nonce = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    fixtures = c.load_fixtures()
    t46, tn = c.names(46), c.names(nonce)
    work = tempfile.mkdtemp(dir="/fast/scratch/hyaku/mado-r46/ExecDoNothingC1", prefix="verify-")
    ok_all = 0
    for fx in fixtures:
        res = []
        for table, variant in ((t46, "A"), (t46, "B"), (tn, "A")):
            d = tempfile.mkdtemp(dir=work, prefix="c-")
            raw = None
            if fx["dump_bytes"]:
                raw = fx["dump"].encode("latin-1")
                raw = c.BIG_DUMP if raw == b"@BIGDUMP" else raw
            else:
                raw = json.dumps(c.subst(fx["dump"], table), indent=2).encode()
            dp = os.path.join(d, "devices.json")
            open(dp, "wb").write(raw)
            data = None
            if fx["stdin"]:
                args, data = ["--devices", "-"], raw
            else:
                args = ["--devices", dp]
            cfgs = fx["configs"]
            if cfgs == "usage":
                args = ["--devices", dp]
            elif cfgs is None:
                cdir = os.path.join(d, "conf.d")
                os.makedirs(cdir)
                args += ["--config", cdir]
            else:
                for k, text in enumerate(cfgs):
                    cp = os.path.join(d, "c%d.conf" % k)
                    with open(cp, "w", newline="", encoding="utf-8") as f:
                        f.write(c.BIG_CONFIG if text == "@BIG" else c.subst(text, table))
                    args += ["--config", cp]
            env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": d,
                   "HYPRLAND_INSTANCE_SIGNATURE": "mado-r46-fixture"}
            p = subprocess.run([sys.executable, "-I", tool] + args, input=data, capture_output=True, env=env,
                               timeout=20, cwd=d)
            want = "".join(c.subst(l, table) + "\n" for l in fx["expect"])
            ok = p.returncode == fx["rc"] and p.stdout.decode() == want and p.stderr == b""
            res.append((ok, p.returncode, p.stdout.decode()[-200:]))
        ok = all(r[0] for r in res)
        ok_all += ok
        if not ok:
            bad = [lab for lab, r in zip(("46A", "46B", "nA"), res) if not r[0]]
            print("FAIL %-34s %s rc=%s" % (fx["label"], ",".join(bad), [r[1] for r in res]))
    print("LOCAL: fixtures=%d/%d" % (ok_all, len(fixtures)))
    print("work=%s" % work)


if __name__ == "__main__":
    main()
