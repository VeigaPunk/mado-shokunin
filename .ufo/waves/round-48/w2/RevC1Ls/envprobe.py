#!/usr/bin/env python3
"""RevC1Ls: which ls-environment variables really move the hash, and which the tool merely refuses.

Baseline: the pin's gen_hash on one tree. Then each variable is added to the SAME env: does the pin's hash
move (the guard is justified), and what does the frozen tool do (predict, or MADO_TERM_OUT_OF_CONTRACT)?
"""
import json
import os
import sys
import time

S = "/fast/scratch/hyaku/mado-r48/RevC1Ls"
sys.path.insert(0, S + "/run")
import driver as D
import matrix as M

VARS = [("LS_COLORS", "rs=0:di=01;34"), ("TIME_STYLE", "long-iso"), ("POSIXLY_CORRECT", "1"),
        ("BLOCK_SIZE", "512"), ("LS_BLOCK_SIZE", "512"), ("QUOTING_STYLE", "escape"), ("COLUMNS", "40"),
        ("TZ", "Europe/Berlin")]


def pin_hash(root, env):
    D.stale_cache(root)
    rc, out, err = D.pin_run(root, env)
    for line in err.decode("utf-8", "surrogateescape").split("\n"):
        if "got fresh hash '" in line:
            return line.split("got fresh hash '")[1].split("'")[0], rc
    return None, rc


def main():
    root = os.path.join(S, "run", "envprobe", "r")
    os.system("rm -rf " + os.path.join(S, "run", "envprobe"))
    os.makedirs(root)
    env = M.wtree(root, "plain")
    os.environ["TZ"] = env["TZ"]
    time.tzset()
    base, _ = pin_hash(root, env)
    os.environ["TZ"] = env["TZ"]
    time.tzset()
    tool_base, _o, _e = D.tool_hash(root, env)
    rows = [{"var": "-", "pin_hash": base, "moved": False, "tool": tool_base, "tool_ok": tool_base == base}]
    print("baseline pin=%s tool=%s" % (base, tool_base))
    for k, v in VARS:
        e = dict(env, **{k: v})
        os.environ["TZ"] = e["TZ"]          # the tool reads TZ from the process environment (os.environ)
        time.tzset()
        h, rc = pin_hash(root, e)
        th, _ops, terr = D.tool_hash(root, e)
        rows.append({"var": k, "value": v, "pin_hash": h, "pin_rc": rc, "moved": h != base,
                     "tool": th, "tool_err": terr, "tool_ok": th == h})
        print("%-16s %-12s pin_moved=%-5s pin_rc=%d tool=%s" % (k, v, h != base, rc,
                                                                terr or ("match" if th == h else "DIFF")))
    json.dump(rows, open(S + "/run/envprobe.json", "w"), indent=1)
    os.system("sudo -n rm -rf -- " + os.path.join(S, "run", "envprobe"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
