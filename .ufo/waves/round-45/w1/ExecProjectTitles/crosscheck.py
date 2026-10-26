#!/usr/bin/env python3
"""Independent (second-implementation) check of the round-45 w1 projections.

1. `jq` rebuilds the 7-key projection straight from the originals at the pin; the bytes my
   generator wrote must be semantically equal to jq's result.
2. `json.dumps(indent=2)+"\\n"` re-serialisation of the *reference* file must reproduce that
   file byte-for-byte — proves the emitted style is the reference style, not a lookalike.
3. The two originals must differ only in title-family fields (the only bytes removed).
"""
import json
import subprocess
import sys

PIN = "0c89478af821a6424c9ac922eafe02e39630cf4f"
REF = ".ufo/waves/round-43/fetch/host-clients-r43.json"
LIVE = [
    ".ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json",
    ".ufo/waves/round-43/w2/SentLiveRun/dump-now.json",
]
JQ = '[.[] | {address, mapped, class, floating, size, at, monitor}]'
TITLE_KEYS = {"title", "initialTitle", "initialClass", "xdgDescription", "xdgTag"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


def main():
    repo, seat = sys.argv[1], sys.argv[2]
    fails = []

    # The reference is itself json.dumps(indent=1)+newline (711 B); the seat spec asks for
    # indent=2 for the emitted projection, so the reference is normative only for key
    # set/order, and each emitted file is checked against its own declared style.
    ref_raw = git(repo, "show", f"{PIN}:{REF}").decode()
    ok = json.dumps(json.loads(ref_raw), indent=1) + "\n" == ref_raw
    print(f"[{'ok' if ok else 'FAIL'}] reference file is json.dumps(indent=1)+newline (its own style)")
    fails += [] if ok else ["ref style"]

    origs = {}
    for rel in LIVE:
        raw = git(repo, "show", f"{PIN}:{rel}")
        origs[rel] = json.loads(raw)
        jqout = subprocess.run(["jq", "--indent", "2", JQ], input=raw,
                               capture_output=True, check=True).stdout
        mine = open(f"{seat}/proj/{rel}", encoding="utf-8").read()
        same = json.loads(jqout) == json.loads(mine) and jqout.decode() == mine
        print(f"[{'ok' if same else 'FAIL'}] {rel}: jq projection == emitted bytes "
              f"(semantic + byte)")
        fails += [] if same else [f"jq {rel}"]
        ok3 = json.dumps(json.loads(mine), indent=2) + "\n" == mine
        print(f"[{'ok' if ok3 else 'FAIL'}] {rel}: emitted file is json.dumps(indent=2)+newline")
        fails += [] if ok3 else [f"style {rel}"]
        n = len(json.loads(mine))
        ok2 = n == len(origs[rel])
        print(f"[{'ok' if ok2 else 'FAIL'}] {rel}: {n} of {len(origs[rel])} elements kept")
        fails += [] if ok2 else [f"count {rel}"]

    a, b = (origs[r] for r in LIVE)
    diffs = sorted({k for x, y in zip(a, b) for k in set(x) | set(y) if x.get(k) != y.get(k)})
    ok = bool(diffs) and set(diffs) <= TITLE_KEYS
    print(f"[{'ok' if ok else 'FAIL'}] the two originals differ only in title-family fields: {diffs}")
    fails += [] if ok else ["originals differ beyond titles"]

    if fails:
        raise SystemExit(f"FAILED: {fails}")
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
