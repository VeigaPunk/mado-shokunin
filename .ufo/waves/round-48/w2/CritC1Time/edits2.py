#!/usr/bin/env python3
"""CritC1Time part 2 (v2): same-minute vs cross-minute same-size edit, tool vs pin on the SAME tree+cache state.

The resolver rewrites its cache on every cold run, so after the scored pin run the cache holds the post-edit
state; the tool is therefore scored against the pre-edit cache bytes restored on the same tree (what the pin
itself read when it printed), which is exactly the counter's `prime` + `after` + scored-run shape.
"""
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, "/fast/scratch/hyaku/mado-r48/CritC1Time")
import harness as H
import edits as E

PIN = H.PIN
TOOLP = H.TOOLP
S = H.S


def fresh(root):
    shutil.rmtree(root, ignore_errors=True)
    H.build_tree(root)
    with open(os.path.join(root, "bin/fool"), "wb") as fh:
        fh.write(H.STUB)
    os.chmod(os.path.join(root, "bin/fool"), 0o755)


def cache_path(root):
    return os.path.join(root, ".rw/cache/xdg-terminal-exec")


def pin_plain(root, tz, debug=False):
    env = H.env_for(root, tz, root + "/.rw/cache")
    if debug:
        env["XTE_DEBUG"] = "1"
    r = subprocess.run([PIN, "--print-cmd"], env=env, capture_output=True, timeout=60)
    return r.returncode, r.stdout.decode("utf-8", "surrogateescape"), r.stderr.decode("utf-8", "surrogateescape")


def tool_print(root, tz):
    env = H.env_for(root, tz, root + "/.rw/cache")
    r = subprocess.run([sys.executable, "-I", TOOLP, "print", "--print-cmd"], env=env,
                       capture_output=True, timeout=60)
    return r.returncode, r.stdout.decode("utf-8", "surrogateescape"), r.stderr.decode("utf-8", "surrogateescape")


def wait_same_minute_window():
    """Return a time t that is this minute and at least 4 s old, sleeping briefly if the minute just turned."""
    for _ in range(130):
        now = time.time_ns() // 1000000000
        if now % 60 >= 4:
            return now, now - 3
        time.sleep(0.5)
    now = time.time_ns() // 1000000000
    return now, now - 3


def run(tz, same_minute):
    root = os.path.join(S, "ed2-" + tz.replace("/", "_") + ("-same" if same_minute else "-cross"))
    fresh(root)
    if same_minute:
        now, t = wait_same_minute_window()
    else:
        now = time.time_ns() // 1000000000
        t = now - 60 - (now % 60)     # the previous minute
    H.set_times(root, t)
    prime = pin_plain(root, tz)
    pre_cache = open(cache_path(root), "rb").read()
    pre_hash = pre_cache.split(b"\n")[0].decode()
    E.edit_same_size(root)
    os.utime(os.path.join(root, "usr/share/applications/foot.desktop"), (now, now))
    d_before = time.strftime("%b %e %H:%M", time.localtime(t))
    d_after = time.strftime("%b %e %H:%M", time.localtime(now))
    scored = pin_plain(root, tz, debug=True)         # the pin's own answer on the edited tree + old cache
    post_rc, post_out, post_err = scored
    state = ("hit" if "cache is actual" in post_err else
             "stale" if "cache is out-of-date" in post_err else "other")
    # restore the pre-edit cache: the tool must predict the pin's answer from the same state
    with open(cache_path(root), "wb") as fh:
        fh.write(pre_cache)
    tp = tool_print(root, tz)
    agree = (tp[0] == post_rc and tp[1] == post_out)
    return {"tz": tz, "case": "same-minute" if same_minute else "cross-minute",
            "prime_mtime": t, "edit_mtime": now,
            "date_before": d_before, "date_after": d_after, "same_date_string": d_before == d_after,
            "prime_rc": prime[0], "prime_stdout": prime[1], "prime_hash": pre_hash,
            "pin_state": state, "pin_rc": post_rc, "pin_stdout": post_out,
            "tool_rc": tp[0], "tool_stdout": tp[1], "tool_stderr": tp[2][:120],
            "agree": agree}


def main():
    tz = sys.argv[1]
    rows = [run(tz, True), run(tz, False)]
    with open(os.path.join(S, "ed2-%s.json" % tz.replace("/", "_")), "w") as fh:
        json.dump(rows, fh, indent=1)
    print(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
