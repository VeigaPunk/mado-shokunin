#!/usr/bin/env python3
"""Independent re-check of a fixtures.json: recompile every distinct RMLVO from
the fixture metadata into a FRESH work dir (clean env) and re-run the pinned
judge once per fixture, comparing stdout+rc to the stored expect.

This is the counter's procedure, run by the seat as a self-check.
"""
import argparse
import collections
import json
import os
import subprocess
import sys

COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--fixtures", required=True)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    if work == "/tmp" or work.startswith("/tmp/"):
        sys.exit("refusing a work dir under /tmp")
    os.makedirs(os.path.join(work, "km"), exist_ok=True)
    os.makedirs(os.path.join(work, "w", "cfg"), exist_ok=True)
    env = {"PATH": "/usr/bin", "HOME": os.path.join(work, "w"),
           "XDG_CONFIG_HOME": os.path.join(work, "w", "cfg")}

    fixtures = json.load(open(a.fixtures, encoding="utf-8"))
    kmpath = {}
    for f in fixtures:
        key = tuple(f["rmlvo"][k] for k in ("rules", "model", "layout", "variant", "options"))
        if key in kmpath:
            continue
        p = os.path.join(work, "km", "%d.xkb" % len(kmpath))
        cmd = [COMPILE]
        for name, val in zip(("rules", "model", "layout", "variant", "options"), key):
            if val:
                cmd += ["--" + name, val]
        with open(p, "wb") as out:
            r = subprocess.run(cmd, stdout=out, stderr=subprocess.DEVNULL, env=env)
        if r.returncode != 0:
            sys.exit("compile failed for %s" % (key,))
        kmpath[key] = p

    ok = collections.Counter()
    bad = []
    for f in fixtures:
        key = tuple(f["rmlvo"][k] for k in ("rules", "model", "layout", "variant", "options"))
        r = subprocess.run([JUDGE, "--keymap=" + kmpath[key], "--disable-compose",
                            "--keysym", f["arg"]],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)
        if r.returncode == f["expect"]["rc"] and r.stdout.decode("utf-8") == f["expect"]["stdout"]:
            ok[f["class"]] += 1
        else:
            bad.append((f["id"], f["class"], f["arg"], f["expect"]["rc"], r.returncode,
                        len(f["expect"]["stdout"]), len(r.stdout)))

    per = collections.Counter(f["class"] for f in fixtures)
    for cls in sorted(per):
        print("%-9s %3d/%3d" % (cls, ok[cls], per[cls]))
    print("TOTAL     %3d/%3d  keymaps=%d mismatches=%d"
          % (sum(ok.values()), len(fixtures), len(kmpath), len(bad)))
    for b in bad[:20]:
        print("MISMATCH", b)
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
