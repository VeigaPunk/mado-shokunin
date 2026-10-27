#!/usr/bin/env python3
"""probe-mtime.py - what an mtime bump does to the resolver's cache hash (old-date form).

Writes mtime-receipt.txt beside this file. Reuses gen.py's sandbox. Scratch: --work.
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen  # noqa: E402

WORK = "/fast/scratch/hyaku/mado-r48/ExecFixturesV2/probe-mtime"
BASE = {
    "id": "mt-probe", "class": "PROBE", "env": dict(gen.ENV_BASE),
    "files": {gen.LIST: "foot.desktop\n", gen.APP + "/foot.desktop": gen.entry()},
    "exec": ["bin/foot"], "args": ["--print-cmd"], "prime": {"args": ["--print-cmd"]},
    "mtime": gen.MT, "expect": None, "meta": {},
}
DELTAS = [0, 59, 60, 61, 3600, 43200, 86340, 86400]


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    box = gen.Box(WORK)
    lines = []
    prime_out = None
    for d in DELTAS:
        case = json.loads(json.dumps(BASE))
        case["after"] = {"mtime": gen.MT + d}
        root = os.path.join(WORK, "d%06d/r" % d)
        rc, out, err, order = gen.run_trial(box, case, root, cached=True)
        state = gen.cache_state_from(err)
        ls_date = subprocess.run(["ls", "-l", "--time-style=long-iso", os.path.join(root, gen.APP)],
                                 capture_output=True).stdout.decode().split("\n")
        st = [l for l in ls_date if "foot.desktop" in l]
        if prime_out is None:
            prime_out = out
        lines.append("delta=%6d state=%-8s rc=%d stdout_equal_to_prime=%s ls=%r"
                     % (d, state, rc, out == prime_out, st[0][:70] if st else ""))
        shutil.rmtree(os.path.join(WORK, "d%06d" % d), ignore_errors=True)
    # what the sandboxed `ls -l` shows for the same two mtimes (no /etc, numeric ids)
    body = ("probe-mtime: xdg-terminal-exec 0.14.3 cache-hash sensitivity to an mtime bump\n"
            "seed mtime = %d (2020-01-01T00:00:00Z, the old-date form)\n"
            "pin sha256 = %s\n"
            "each row: prime at seed mtime, re-pin every file+dir to seed+delta, scored --print-cmd with XTE_DEBUG=1\n"
            "state is the resolver's own cache verdict (D: cache is actual / out-of-date)\n\n" % (gen.MT, gen.PIN_SHA256)
            + "\n".join(lines) + "\n")
    open(os.path.join(HERE, "mtime-receipt.txt"), "w").write(body)
    print(body)


main()
