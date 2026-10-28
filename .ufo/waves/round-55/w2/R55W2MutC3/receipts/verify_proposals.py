#!/usr/bin/env python3
"""Check the text-proposed kill tests for the survivors: each proposal is a one-edit input built as a NEW ctl commit in the
scratch repo (never the lane). Runs the UNCHANGED counter and each survivor mutant on it."""
import json
import os
import subprocess

S = "/fast/scratch/hyaku/mado-r55/R55W2MutC3"
D = open(os.path.join(S, "env.sh")).read().split("=", 1)[1].strip()
G = open(os.path.join(S, "good.rev")).read().strip()
d = json.load(open(os.path.join(S, "summary.json")))
DELIV = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w2/R55W2MutC3/mutants"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C", "HOME": S,
       "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}


def git(*a, inp=None):
    p = subprocess.run(["git", "-C", D] + list(a), input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    assert p.returncode == 0, p.stderr
    return p.stdout


assert git("rev-parse", "--show-toplevel").decode().strip() == D
base_entry = git("show", G + ":" + ENTRY)


def commit_with(entry_bytes, tag):
    idx = os.path.join(S, "idx-%s" % tag)
    if os.path.exists(idx):
        os.unlink(idx)
    env2 = dict(env, GIT_INDEX_FILE=idx)
    subprocess.run(["git", "-C", D, "read-tree", G], env=env2, check=True)
    blob = git("hash-object", "-w", "--stdin", inp=entry_bytes).decode().strip()
    subprocess.run(["git", "-C", D, "update-index", "--cacheinfo", "100644,%s,%s" % (blob, ENTRY)], env=env2, check=True)
    tree = subprocess.run(["git", "-C", D, "write-tree"], env=env2, stdout=subprocess.PIPE, check=True).stdout.decode().strip()
    sha = git("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit-tree", tree, "-p", G, "-m", tag,
              inp=b"").decode().strip()
    os.unlink(idx)
    return sha


def on_p23(e, old, new):
    out = []
    n = 0
    for ln in e.split(b"\n"):
        if ln.startswith(b"| P23 |"):
            n += ln.count(old.encode())
            ln = ln.replace(old.encode(), new.encode())
        out.append(ln)
    assert n >= 1, old
    return b"\n".join(out)


def heading_off(e):
    old = b"## Correction (round 55): P23 supersedes P19"
    assert e.count(old) == 1
    return e.replace(old, b"Correction (round 55): P23 supersedes P19")


proposals = {
    "V1 paraphrase 'Only when' paragraph, no verbatim P19 sentence": base_entry + b"\nOnly when `m_passPressed == 1` does `Actions::pass` send a PRESSED keyboard key.\n",
    "V2 P23 row: RELEASED -> released": on_p23(base_entry, "RELEASED", "released"),
    "V3 P23 row: '== 1' -> 'is 1'": on_p23(base_entry, "== 1", "is 1"),
    "V4 P23 row: m_passPressed -> passPressed": on_p23(base_entry, "m_passPressed", "passPressed"),
    "V5 P23 row: 'any other value' -> 'remaining value' (else kept)": on_p23(base_entry, "any other value", "remaining value"),
    "V6 P23 row: Pin:anchor 1554-1576 -> 1554-1558": on_p23(base_entry, "Hyprland-ConfigActions.cpp:1554-1576", "Hyprland-ConfigActions.cpp:1554-1558"),
    "V7 heading without ATX marker": heading_off(base_entry),
}
survivors = ["C09", "C11", "C13", "C14", "C15", "C17", "C31", "C37"]
counters = {"unchanged": os.path.join(S, "quality/counters/c3-r55-p19.py")}
for mid in survivors:
    counters[mid] = os.path.join(DELIV, d["counters"][mid]["file"])

rows = []
for i, (name, entry) in enumerate(proposals.items()):
    sha = commit_with(entry, "V%d" % (i + 1))
    line = {}
    for cname, cpath in counters.items():
        w = os.path.join(S, "runs", "verify", "V%d-%s" % (i + 1, cname))
        os.makedirs(w, exist_ok=True)
        p = subprocess.run(["python3", "-I", cpath, "--repo", D, "--rev", sha, "--work", w], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, env=env, stdin=subprocess.DEVNULL)
        out = p.stdout.decode().strip().splitlines()
        t = out[-1].split("verdict=")[1] if out and "verdict=" in out[-1] else "SETUP/CRASH rc=%d" % p.returncode
        line[cname] = t
    rows.append((name, sha[:10], line))
    print(name, sha[:10], json.dumps(line), flush=True)
json.dump(rows, open(os.path.join(S, "verify.json"), "w"), indent=1)
print("VERIFY DONE")
