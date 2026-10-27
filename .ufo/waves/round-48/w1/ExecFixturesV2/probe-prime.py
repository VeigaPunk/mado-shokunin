#!/usr/bin/env python3
"""probe-prime.py - does the resolver's background `save_cache "$1" &` (x:1457) survive the sandbox?

The counter's Box runs the pin as PID 1 of the bwrap PID namespace. When PID 1 exits the kernel kills the rest of
the namespace, so the background save is killed with it. This probe measures both shapes: pin as PID 1 (like a scored
run) and pin under a bash parent that waits for the cache file (the priming recipe in prime-wrap.sh).
Writes prime-receipt.txt beside this file.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen  # noqa: E402

WORK = "/fast/scratch/hyaku/mado-r48/ExecFixturesV2/probe-prime"
CASE = {
    "id": "prime-probe", "env": dict(gen.ENV_BASE),
    "files": {gen.LIST: "foot.desktop\n", gen.APP + "/foot.desktop": gen.entry()},
    "exec": ["bin/foot"], "args": ["--print-cmd"], "mtime": gen.MT,
}


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    box = gen.Box(WORK)
    rows = []
    direct_hit = 0
    wrap_hit = 0
    body = ""
    for i in range(6):
        for mode in ("direct", "wrapped"):
            root = os.path.join(WORK, "%s-%d/r" % (mode, i))
            gen.materialize(root, CASE, with_cache=False)
            env = gen.build_env(CASE, root)
            box.run(root, env, ["--print-cmd"], wrap=(mode == "wrapped"))
            cache = os.path.join(root, ".rw/cache/xdg-terminal-exec")
            ok = os.path.exists(cache)
            size = os.path.getsize(cache) if ok else -1
            if mode == "direct" and ok:
                direct_hit += 1
            if mode == "wrapped" and ok:
                wrap_hit += 1
            if mode == "wrapped" and i == 0 and ok:
                body = open(cache, encoding="utf-8", errors="surrogateescape").read()
            rows.append("%-7s trial=%d cache=%s bytes=%d" % (mode, i, "present" if ok else "ABSENT", size))
            shutil.rmtree(os.path.join(WORK, "%s-%d" % (mode, i)), ignore_errors=True)
    text = ("probe-prime: xdg-terminal-exec 0.14.3 `save_cache \"$1\" &` under the C1 sandbox\n"
            "pin sha256 = %s\n"
            "direct  = the pin is PID 1 of the bwrap namespace (exactly what a scored counter run does)\n"
            "wrapped = /bin/bash -c '<pin> \"$@\"; wait for the cache to end with RS+END_OF_EXEC_USEP; exit rc' "
            "(prime-wrap.sh)\n\n" % gen.PIN_SHA256
            + "\n".join(rows) + "\n\n"
            + "direct cache present: %d/6\nwrapped cache present: %d/6\n\n" % (direct_hit, wrap_hit)
            + "wrapped cache body (trial 0), %d bytes:\n%r\n" % (len(body), body))
    open(os.path.join(HERE, "prime-receipt.txt"), "w").write(text)
    print(text)


main()
